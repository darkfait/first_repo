# -*- coding: utf-8 -*-
'''
2. add_data.py - с помощью этого скрипта, выполняется добавление данных в БД. 
Скрипт должен добавлять данные из вывода sh ip dhcp snooping binding и информацию о коммутаторах

Соответственно, в файле add_data.py должны быть две части:
* информация о коммутаторах добавляется в таблицу switches
 * данные о коммутаторах, находятся в файле switches.yml
* информация на основании вывода sh ip dhcp snooping binding добавляется в таблицу dhcp
 * вывод с трёх коммутаторов:
   * файлы sw1_dhcp_snooping.txt, sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt
 * так как таблица dhcp изменилась, и в ней теперь присутствует поле switch, его нужно также заполнять. Имя коммутатора определяется по имени файла с данными

Пример выполнения скрипта, когда база данных еще не создана:
$ python add_data.py
База данных не существует. Перед добавлением данных, ее надо создать

Пример выполнения скрипта первый раз, после создания базы данных:
$ python add_data.py
Добавляю данные в таблицу switches...
Добавляю данные в таблицу dhcp...

Пример выполнения скрипта, после того как данные были добавлены в таблицу (порядок добавления данных может быть произвольным, но сообщения должны выводиться аналогично выводу ниже):
$ python add_data.py
Добавляю данные в таблицу switches...
При добавлении данных: ('sw1', 'London, 21 New Globe Walk') Возникла ошибка: UNIQUE constraint failed: switches.hostname
При добавлении данных: ('sw2', 'London, 21 New Globe Walk') Возникла ошибка: UNIQUE constraint failed: switches.hostname
При добавлении данных: ('sw3', 'London, 21 New Globe Walk') Возникла ошибка: UNIQUE constraint failed: switches.hostname
Добавляю данные в таблицу dhcp...
При добавлении данных: ('00:09:BB:3D:D6:58', '10.1.10.2', '10', 'FastEthernet0/1', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:04:A3:3E:5B:69', '10.1.5.2', '5', 'FastEthernet0/10', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:05:B3:7E:9B:60', '10.1.5.4', '5', 'FastEthernet0/9', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:07:BC:3F:A6:50', '10.1.10.6', '10', 'FastEthernet0/3', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:09:BC:3F:A6:50', '192.168.100.100', '1', 'FastEthernet0/7', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:E9:BC:3F:A6:50', '100.1.1.6', '3', 'FastEthernet0/20', 'sw3') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:E9:22:11:A6:50', '100.1.1.7', '3', 'FastEthernet0/21', 'sw3') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:A9:BB:3D:D6:58', '10.1.10.20', '10', 'FastEthernet0/7', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:B4:A3:3E:5B:69', '10.1.5.20', '5', 'FastEthernet0/5', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:C5:B3:7E:9B:60', '10.1.5.40', '5', 'FastEthernet0/9', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:A9:BC:3F:A6:50', '10.1.10.60', '20', 'FastEthernet0/2', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac


На данном этапе, оба скрипта вызываются без аргументов.

Код в скриптах должен быть разбит на функции.
Какие именно функции и как разделить код, надо решить самостоятельно.
Часть кода может быть глобальной.

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
    sw_name = dhcp_fname[:dhcp_fname.find('_dhcp')]
    regex_data = r'([\w:]+) +([\d.]+).+? dhcp-snooping +(\d+) +(\S+)'
    with open(dhcp_fname) as f:
        match_iter = re.finditer(regex_data,f.read())
        values_list = []
        for match in match_iter:
            mac,ip,vlan,iface = match.groups()
            values_list.append([mac, ip, vlan, iface, sw_name])
    return(values_list)


   
my_db_file_name = 'dhcp_snooping.db'
switches_data = 'switches.yml'
dhcp_files_list = ['sw1_dhcp_snooping.txt', 'sw2_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt']


if not file_check(my_db_file_name):
    print('База данных не существует. Перед добавлением данных, ее надо создать')
else:
    connect = sqlite3.connect(my_db_file_name)
    #ADD DATA TO SWITCHES TABLE
    print('Добавляю данные в таблицу switches...')
    for sw_data in list_data_switches(switches_data):
        try:
            with connect:
                query_sw = "INSERT into switches values (?, ?)"
                connect.execute(query_sw,sw_data)
        except sqlite3.IntegrityError as err:
            print('При добавлении данных: ', sw_data, 'Возникла ошибка: ', err)
    #ADD DATA TO DHCP TABLE
    print('Добавляю данные в таблицу dhcp...')
    for dhcp_file in dhcp_files_list:
        for dhcp_data in list_data_dhcp(dhcp_file):
            try:
                with connect:
                    query_dhcp = "INSERT into dhcp values (?, ?, ?, ?, ?)"
                    connect.execute(query_dhcp,dhcp_data)
            except sqlite3.IntegrityError as err:
                print('При добавлении данных: ', dhcp_data, 'Возникла ошибка: ', err)
    connect.close()
      
'''sqlite3.IntegrityError'''

'''информация на основании вывода sh ip dhcp snooping binding добавляется в таблицу dhcp

    вывод с трёх коммутаторов: файлы sw1_dhcp_snooping.txt, sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt
    так как таблица dhcp изменилась, и в ней теперь присутствует поле switch, его нужно также заполнять. 
    Имя коммутатора определяется по имени файла с данными
    

| dhcp (\n    mac          text primary key,
\n    ip           text,
\n    vlan         text,
\n    interface    text,
\n    switch       text not null references switches(hostname)\n) |
'''

'''
    MacAddress          IpAddress        Lease(sec)  Type           VLAN  Interface
------------------  ---------------  ----------  -------------  ----  --------------------
00:09:BB:3D:D6:58   10.1.10.2        86250       dhcp-snooping   10    FastEthernet0/1
00:04:A3:3E:5B:69   10.1.5.2         63951       dhcp-snooping   5     FastEthernet0/10
00:05:B3:7E:9B:60   10.1.5.4         63253       dhcp-snooping   5     FastEthernet0/9
00:07:BC:3F:A6:50   10.1.10.6        76260       dhcp-snooping   10    FastEthernet0/3
00:09:BC:3F:A6:50   192.168.100.100  76260       dhcp-snooping   1     FastEthernet0/7
Total number of bindings: 5

'''

'''
    descr_tmp = 'description Connected to {} port {}'
    regex = r'(\w+) +(\w+ [\d/]+) +\d+ +(?:\w )+ +[\w-]+ +(\w+ [\d/]+)'
    with open(file) as f:
        match_iter = re.finditer(regex,f.read())
        for match in match_iter:
            a,b,c = match.groups()
            result[b] = descr_tmp.format(a,c)
    return result
'''


            
            
    

