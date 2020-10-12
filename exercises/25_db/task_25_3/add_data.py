# -*- coding: utf-8 -*-

'''


Задание 25.3

Для заданий 25 раздела нет тестов!

В прошлых заданиях информация добавлялась в пустую БД.
В этом задании, разбирается ситуация, когда в БД уже есть информация.

Скопируйте скрипт add_data.py из задания 25.1 и попробуйте выполнить его повторно, на существующей БД.
Должен быть такой вывод:
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
... (вывод сокращен)

При создании схемы БД, было явно указано, что поле MAC-адрес, должно быть уникальным.
Поэтому, при добавлении записи с таким же MAC-адресом, возникает исключение (ошибка).
В задании 25.1 исключение обрабатывается и выводится сообщение на стандартный поток вывода.

В этом задании считается, что информация периодически считывается с коммутаторов и записывается в файлы.
После этого, информацию из файлов надо перенести в базу данных.
При этом, в новых данных могут быть изменения: MAC пропал, MAC перешел на другой порт/vlan, появился новый MAC и тп.

В этом задании в таблице dhcp надо создать новое поле active, которое будет указывать является ли запись актуальной.
Новая схема БД находится в файле dhcp_snooping_schema.sql

Поле active должно принимать такие значения:
* 0 - означает False. Используется для того, чтобы отметить запись как неактивную
* 1 - True. Используется чтобы указать, что запись активна

Каждый раз, когда информация из файлов с выводом DHCP snooping добавляется заново,
надо пометить все существующие записи (для данного коммутатора), как неактивные (active = 0).
Затем можно обновлять информацию и пометить новые записи, как активные (active = 1).

Таким образом, в БД останутся и старые записи, для MAC-адресов, которые сейчас не активны,
и появится обновленная информация для активных адресов.

Например, в таблице dhcp такие записи:
mac                ip          vlan        interface         switch      active
-----------------  ----------  ----------  ----------------  ----------  ----------
00:09:BB:3D:D6:58  10.1.10.2   10          FastEthernet0/1   sw1         1
00:04:A3:3E:5B:69  10.1.5.2    5           FastEthernet0/10  sw1         1
00:05:B3:7E:9B:60  10.1.5.4    5           FastEthernet0/9   sw1         1
00:07:BC:3F:A6:50  10.1.10.6   10          FastEthernet0/3   sw1         1
00:09:BC:3F:A6:50  192.168.10  1           FastEthernet0/7   sw1         1


И надо добавить такую информацию из файла:
MacAddress          IpAddress        Lease(sec)  Type           VLAN  Interface
------------------  ---------------  ----------  -------------  ----  --------------------
00:09:BB:3D:D6:58   10.1.10.2        86250       dhcp-snooping   10    FastEthernet0/1
00:04:A3:3E:5B:69   10.1.15.2        63951       dhcp-snooping   15    FastEthernet0/15
00:05:B3:7E:9B:60   10.1.5.4         63253       dhcp-snooping   5     FastEthernet0/9
00:07:BC:3F:A6:50   10.1.10.6        76260       dhcp-snooping   10    FastEthernet0/5


После добавления данных таблица должна выглядеть так:
mac                ip               vlan        interface         switch      active
-----------------  ---------------  ----------  ---------------   ----------  ----------
00:09:BC:3F:A6:50  192.168.100.100  1           FastEthernet0/7   sw1         0
00:09:BB:3D:D6:58  10.1.10.2        10          FastEthernet0/1   sw1         1
00:04:A3:3E:5B:69  10.1.15.2        15          FastEthernet0/15  sw1         1
00:05:B3:7E:9B:60  10.1.5.4         5           FastEthernet0/9   sw1         1
00:07:BC:3F:A6:50  10.1.10.6        10          FastEthernet0/5   sw1         1

Новая информация должна перезаписывать предыдущую:
* MAC 00:04:A3:3E:5B:69 перешел на другой порт и попал в другой интерфейс и получил другой адрес
* MAC 00:07:BC:3F:A6:50 перешел на другой порт

Если какого-то MAC-адреса нет в новом файле, его надо оставить в бд со значением active = 0:
* MAC-адреса 00:09:BC:3F:A6:50 нет в новой информации (выключили комп)


Измените скрипт add_data.py таким образом, чтобы выполнялись новые условия и заполнялось поле active.

Код в скрипте должен быть разбит на функции.
Какие именно функции и как разделить код, надо решить самостоятельно.
Часть кода может быть глобальной.

> Для проверки корректности запроса SQL, можно выполнить его в командной строке, с помощью утилиты sqlite3.

Для проверки задания и работы нового поля, сначала добавьте в бд информацию из файлов sw*_dhcp_snooping.txt,
а потом добавьте информацию из файлов new_data/sw*_dhcp_snooping.txt

Данные должны выглядеть так (порядок строк может быть любым)
-----------------  ---------------  --  ----------------  ---  -
00:09:BC:3F:A6:50  192.168.100.100   1  FastEthernet0/7   sw1  0
00:C5:B3:7E:9B:60  10.1.5.40         5  FastEthernet0/9   sw2  0
00:09:BB:3D:D6:58  10.1.10.2        10  FastEthernet0/1   sw1  1
00:04:A3:3E:5B:69  10.1.15.2        15  FastEthernet0/15  sw1  1
00:05:B3:7E:9B:60  10.1.5.4          5  FastEthernet0/9   sw1  1
00:07:BC:3F:A6:50  10.1.10.6        10  FastEthernet0/5   sw1  1
00:E9:BC:3F:A6:50  100.1.1.6         3  FastEthernet0/20  sw3  1
00:E9:22:11:A6:50  100.1.1.7         3  FastEthernet0/21  sw3  1
00:A9:BB:3D:D6:58  10.1.10.20       10  FastEthernet0/7   sw2  1
00:B4:A3:3E:5B:69  10.1.5.20         5  FastEthernet0/5   sw2  1
00:A9:BC:3F:A6:50  10.1.10.65       20  FastEthernet0/2   sw2  1
00:A9:33:44:A6:50  10.1.10.77       10  FastEthernet0/4   sw2  1
-----------------  ---------------  --  ----------------  ---  -

'''


'''

Можно изменить несколько полей за раз:
new_db.db> UPDATE switch set mngmt_ip = '10.255.1.2', mngmt_vid = 255 WHERE hostname = 'sw2'


Когда возникает нарушение условия уникальности поля, выражение с оператором REPLACE:
    удаляет существующую строку, которая вызвала нарушение
    добавляет новую строку
При добавлении записи, для которой не возникает нарушения уникальности поля, REPLACE работает как обычный INSERT

new_db.db> REPLACE INTO switch VALUES ('0080.A8AA.C8CC', 'sw8', 'Cisco 3850', 'London, Green Str', '10.255.1.8', 255);


исправить так, чтобы новые данные заносились с единичкой. а потом уже заменялись на ноль, после "необнаружения" совпадения
upgrade every to 0 then u

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


   
my_db_file_name = 'dhcp_snooping.db'
switches_data = 'switches.yml'
dhcp_files_list = ['sw1_dhcp_snooping.txt', 'sw2_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt']
dhcp_files_list_new = ['new_data/sw1_dhcp_snooping.txt', 'new_data/sw2_dhcp_snooping.txt', 'new_data/sw3_dhcp_snooping.txt']

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
    query_10 = "UPDATE dhcp set active = '0'"
    connect.execute(query_10)
    connect.commit()
    #for dhcp_file in dhcp_files_list:
    for dhcp_file in dhcp_files_list_new:
        for dhcp_data in list_data_dhcp(dhcp_file):
            try:
                with connect:
                    query_dhcp = "INSERT into dhcp values (?, ?, ?, ?, ?, 1)"
                    connect.execute(query_dhcp,dhcp_data)
            except sqlite3.IntegrityError as err:
                #print('При добавлении данных: ', dhcp_data, 'Возникла ошибка: ', err)
                with connect:
                    query_dhcp = "REPLACE into dhcp values (?, ?, ?, ?, ?, 1)"
                    connect.execute(query_dhcp,dhcp_data)
    connect.close()
      

            
    

