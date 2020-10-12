# -*- coding: utf-8 -*-

'''
Задание 25.5a

Для заданий 25 раздела нет тестов!

После выполнения задания 25.5, в таблице dhcp есть новое поле last_active.

Обновите скрипт add_data.py, таким образом, чтобы он удалял все записи,
которые были активными более 7 дней назад.

Для того, чтобы получить такие записи, можно просто вручную обновить поле last_active в некоторых записях и поставить время 7 или более дней.

В файле задания описан пример работы с объектами модуля datetime.
Показано как получить дату 7 дней назад. С этой датой надо будет сравнивать время last_active.

Обратите внимание, что строки с датой, которые пишутся в БД, можно сравнивать между собой.

'''

'''
from datetime import timedelta, datetime

now = datetime.today().replace(microsecond=0)
week_ago = now - timedelta(days=7)

#print(now)
#print(week_ago)
#print(now > week_ago)
#print(str(now) > str(week_ago))
'''


'''
DELETE from switch where hostname = 'sw8'
'''

import sqlite3
import re
import yaml
from pprint import pprint
from datetime import timedelta, datetime

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
    delete_old_data()
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

def delete_old_data():
    now = datetime.today().replace(microsecond=0)
    week_ago = now - timedelta(days=7)
    query_delet_old = "DELETE from dhcp where last_active < ?"
    connect.execute(query_delet_old,(str(week_ago),))
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


