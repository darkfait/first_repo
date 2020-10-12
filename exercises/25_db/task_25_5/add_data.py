# -*- coding: utf-8 -*-

'''
Задание 25.5

Для заданий 25 раздела нет тестов!

После выполнения заданий 25.1 - 25.5 в БД остается информация о неактивных записях.
И, если какой-то MAC-адрес не появлялся в новых записях, запись с ним,
может остаться в БД навсегда.

И, хотя это может быть полезно, чтобы посмотреть, где MAC-адрес находился в последний раз,
постоянно хранить эту информацию не очень полезно.

Например, если запись в БД уже больше месяца, то её можно удалить.
'''

'''
Для того, чтобы сделать такой критерий, нужно ввести новое поле,
в которое будет записываться последнее время добавления записи.

Новое поле называется last_active и в нем должна находиться строка,
в формате: YYYY-MM-DD HH:MM:SS.

В этом задании необходимо:
* изменить, соответственно, таблицу dhcp и добавить новое поле.
 * таблицу можно поменять из cli sqlite, но файл dhcp_snooping_schema.sql тоже необходимо изменить
* изменить скрипт add_data.py, чтобы он добавлял к каждой записи время

Получить строку со временем и датой, в указанном формате, можно с помощью функции datetime в запросе SQL.
Синтаксис использования такой:
sqlite> insert into dhcp (mac, ip, vlan, interface, switch, active, last_active)
   ...> values ('00:09:BC:3F:A6:50', '192.168.100.100', '1', 'FastEthernet0/7', 'sw1', '0', datetime('now'));

То есть вместо значения, которое записывается в базу данных, надо указать datetime('now').

После этой команды в базе данных появится такая запись:
mac                ip               vlan        interface        switch      active      last_active
-----------------  ---------------  ----------  ---------------  ----------  ----------  -------------------
00:09:BC:3F:A6:50  192.168.100.100  1           FastEthernet0/7  sw1         0           2019-03-08 11:26:56
'''


import sqlite3
import re
import yaml
from pprint import pprint

from create_db import file_check




def list_data_switches(switches_data_file):
    with open(switches_data_file) as f:
        sw_data = yaml.safe_load(f)['switches']
        data_switches = []
        for sw_hostname, sw_values in sw_data.items():
            data_switches.append((sw_hostname, sw_values))
    return(data_switches)


def list_data_dhcp(dhcp_fname):
    sw_name = dhcp_fname[dhcp_fname.find('sw'):dhcp_fname.find('_dhcp')]
    regex_data = r'([\w:]+) +([\d.]+).+? dhcp-snooping +(\d+) +(\S+)'
    with open(dhcp_fname) as f:
        match_iter = re.finditer(regex_data,f.read())
        values_list = []
        for match in match_iter:
            mac,ip,vlan,iface = match.groups()
            values_list.append([mac, ip, vlan, iface, sw_name])
    return(values_list)

def add_data_to_switches(switches_file):
    print('Добавляю данные в таблицу switches...')
    for sw_data in list_data_switches(switches_file):
        try:
            with connect:
                query_sw = "INSERT into switches values (?, ?)"
                connect.execute(query_sw,sw_data)
        except sqlite3.IntegrityError as err:
            print('При добавлении данных: ', sw_data, 'Возникла ошибка: ', err)
    return

def add_data_to_DHCP(dhcp_files_list):
    print('Добавляю данные в таблицу dhcp...')
    query_10 = "UPDATE dhcp set active = '0'"
    connect.execute(query_10)
    connect.commit()
    for dhcp_file in dhcp_files_list:
        for dhcp_data in list_data_dhcp(dhcp_file):
            try:
                with connect:
                    query_dhcp = "INSERT into dhcp values (?, ?, ?, ?, ?, 1,datetime('now'))"
                    connect.execute(query_dhcp,dhcp_data)
            except sqlite3.IntegrityError as err:
                #print('При добавлении данных: ', dhcp_data, 'Возникла ошибка: ', err)
                with connect:
                    query_dhcp = "REPLACE into dhcp values (?, ?, ?, ?, ?, 1,datetime('now'))"
                    connect.execute(query_dhcp,dhcp_data)
    return


my_db_file_name = 'dhcp_snooping.db'
switches_data_file = 'switches.yml'
my_dhcp_files_list = ['sw1_dhcp_snooping.txt', 'sw2_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt']
my_dhcp_files_list_new = ['new_data/sw1_dhcp_snooping.txt', 'new_data/sw2_dhcp_snooping.txt', 'new_data/sw3_dhcp_snooping.txt']

if not file_check(my_db_file_name):
    print('База данных не существует. Перед добавлением данных, ее надо создать')
else:
    connect = sqlite3.connect(my_db_file_name)
    #ADD DATA TO SWITCHES TABLE
    add_data_to_switches(switches_data_file)
    #ADD DATA TO DHCP TABLE
    add_data_to_DHCP(my_dhcp_files_list_new)
    connect.close()


