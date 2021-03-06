# -*- coding: utf-8 -*-
"""
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный файл коммутатора
и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов, а значения access VLAN:
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов, а значения список разрешенных VLAN:
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt


Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

def get_int_vlan_map(config_filename):
    dict_tr = {}
    dict_ac = {}
    with open(config_filename) as conf_file:
        for line in conf_file:
            if line.strip().startswith('interface '): intf = line.split()[1]
            elif 'trunk allowed vlan' in line:
                dict_tr[intf] = [int(nvlan) for nvlan in line.split()[-1].split(',')]
            elif 'switchport access vlan' in line:
                dict_ac[intf] = int(line.split()[-1])
    print((dict_ac,dict_tr))
    return((dict_ac,dict_tr))

get_int_vlan_map('config_sw1.txt')
