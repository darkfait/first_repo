# -*- coding: utf-8 -*-

'''
В этом задании необходимо создать скрипт get_data.py.

Скрипту могут передаваться аргументы и, в зависимости от аргументов, надо выводить разную информацию.
Если скрипт вызван:
* без аргументов, вывести всё содержимое таблицы dhcp
* с двумя аргументами, вывести информацию из таблицы dhcp, которая соответствует полю и значению
* с любым другим количеством аргументов, вывести сообщение, что скрипт поддерживает только два или ноль аргументов
'''

import sqlite3
import sys

keys = ('mac', 'ip', 'vlan', 'interface', 'switch')
my_db_file = 'dhcp_snooping.db'

def get_data_key_val(file_db, key, val):
    connect = sqlite3.connect(file_db)
    query_kv = 'SELECT * from dhcp WHERE {} = ?'.format(key)
    print(('Информация об устройствах с такими параметрами: {}  {}').format(key,val))
    result = connect.execute(query_kv,(val,))
    return(result)

def get_data_all(file_db):
    connect = sqlite3.connect(file_db)
    query_all = 'SELECT * from dhcp'
    result = connect.execute(query_all)
    return(result)


if len(sys.argv) == 1: 
    print('В таблице dhcp такие записи:  ')
    for row in get_data_all(my_db_file):
        print(row)
elif len(sys.argv) == 3:
    db_key, db_val = sys.argv[1:]
    if db_key not in keys:
        print('Данный параметр не поддерживается.\nДопустимые значения параметров: mac, ip, vlan, interface, switch')
    else:
        for row in get_data_key_val(my_db_file,db_key,db_val):
            print(row)
else:
    print('Пожалуйста, введите два или ноль аргументов')
