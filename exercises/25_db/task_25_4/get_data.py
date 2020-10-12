# -*- coding: utf-8 -*-

'''
В этом задании необходимо создать скрипт get_data.py.

Скрипту могут передаваться аргументы и, в зависимости от аргументов, надо выводить разную информацию.
Если скрипт вызван:
* без аргументов, вывести всё содержимое таблицы dhcp
* с двумя аргументами, вывести информацию из таблицы dhcp, которая соответствует полю и значению
* с любым другим количеством аргументов, вывести сообщение, что скрипт поддерживает только два или ноль аргументов
'''

'''
Задание 25.4

Для заданий 25 раздела нет тестов!

Скопировать файл get_data из задания 25.2.
Добавить в скрипт поддержку столбца active, который мы добавили в задании 25.3.

Теперь, при запросе информации, сначала должны отображаться активные записи,
а затем, неактивные. Если неактивных записей нет, не отображать заголовок "Неактивные записи".

Примеры выполнения итогового скрипта
$ python get_data.py
В таблице dhcp такие записи:

Активные записи:

-----------------  ----------  --  ----------------  ---  -
00:09:BB:3D:D6:58  10.1.10.2   10  FastEthernet0/1   sw1  1
00:04:A3:3E:5B:69  10.1.15.2   15  FastEthernet0/15  sw1  1
00:05:B3:7E:9B:60  10.1.5.4     5  FastEthernet0/9   sw1  1
00:07:BC:3F:A6:50  10.1.10.6   10  FastEthernet0/5   sw1  1
00:E9:BC:3F:A6:50  100.1.1.6    3  FastEthernet0/20  sw3  1
00:E9:22:11:A6:50  100.1.1.7    3  FastEthernet0/21  sw3  1
00:A9:BB:3D:D6:58  10.1.10.20  10  FastEthernet0/7   sw2  1
00:B4:A3:3E:5B:69  10.1.5.20    5  FastEthernet0/5   sw2  1
00:A9:BC:3F:A6:50  10.1.10.65  20  FastEthernet0/2   sw2  1
00:A9:33:44:A6:50  10.1.10.77  10  FastEthernet0/4   sw2  1
-----------------  ----------  --  ----------------  ---  -

Неактивные записи:

-----------------  ---------------  -  ---------------  ---  -
00:09:BC:3F:A6:50  192.168.100.100  1  FastEthernet0/7  sw1  0
00:C5:B3:7E:9B:60  10.1.5.40        5  FastEthernet0/9  sw2  0
-----------------  ---------------  -  ---------------  ---  -

$ python get_data.py vlan 5

Информация об устройствах с такими параметрами: vlan 5

Активные записи:

-----------------  ---------  -  ---------------  ---  -
00:05:B3:7E:9B:60  10.1.5.4   5  FastEthernet0/9  sw1  1
00:B4:A3:3E:5B:69  10.1.5.20  5  FastEthernet0/5  sw2  1
-----------------  ---------  -  ---------------  ---  -

Неактивные записи:

-----------------  ---------  -  ---------------  ---  -
00:C5:B3:7E:9B:60  10.1.5.40  5  FastEthernet0/9  sw2  0
-----------------  ---------  -  ---------------  ---  -


$ python get_data.py vlan 10

Информация об устройствах с такими параметрами: vlan 10

Активные записи:

-----------------  ----------  --  ---------------  ---  -
00:09:BB:3D:D6:58  10.1.10.2   10  FastEthernet0/1  sw1  1
00:07:BC:3F:A6:50  10.1.10.6   10  FastEthernet0/5  sw1  1
00:A9:BB:3D:D6:58  10.1.10.20  10  FastEthernet0/7  sw2  1
00:A9:33:44:A6:50  10.1.10.77  10  FastEthernet0/4  sw2  1
-----------------  ----------  --  ---------------  ---  -
'''


import sqlite3
import sys

keys = ('mac', 'ip', 'vlan', 'interface', 'switch', 'active')
my_db_file = 'dhcp_snooping.db'


def get_data_key_val(file_db, key, val):
    connect = sqlite3.connect(file_db)
    query_kv = 'SELECT * from dhcp WHERE {} = ? AND active = {}'
    result_act = connect.execute(query_kv.format(key,"1"),(val,))
    result_pass = connect.execute(query_kv.format(key,"0"),(val,))
    print(('Информация об устройствах с такими параметрами: {} = {}\n').format(key,val))
    print('Активные записи:\n','-' * 70)
    for row in result_act:
        print(row)
    if result_pass.fetchmany(1):
        result_pass = connect.execute(query_kv.format(key,"0"),(val,))
        print('\nНеактивные записи:\n','-' * 70)
        for row in result_pass:
            print(row)
    return([result_act,result_pass])
    
def get_data_all(file_db):
    query_all = 'SELECT * from dhcp WHERE active = {}'
    connect = sqlite3.connect(file_db)
    result_act = connect.execute(query_all.format("1"))
    result_pass = connect.execute(query_all.format("0"))
    print(result_pass)
    print('Активные записи:\n','-' * 70)
    for row in result_act:
        print(row)
    if result_pass.fetchmany(1):
        result_pass = connect.execute(query_all.format("0"))
        print('\nНеактивные записи:\n','-' * 70)
        for row in result_pass:
            print(row)
    return([result_act,result_pass])
    
if len(sys.argv) == 1: 
    print('В таблице dhcp такие записи:  \n')
    get_data_all(my_db_file)
elif len(sys.argv) == 3:
    db_key, db_val = sys.argv[1:]
    if db_key not in keys:
        print('Данный параметр не поддерживается.\nДопустимые значения параметров: mac, ip, vlan, interface, switch')
    else:
        get_data_key_val(my_db_file,db_key,db_val)
else:
    print('Пожалуйста, введите два или ноль аргументов')
    
