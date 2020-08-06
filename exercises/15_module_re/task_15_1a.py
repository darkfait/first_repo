# -*- coding: utf-8 -*-
"""
Задание 15.1a

Скопировать функцию get_ip_from_cfg из задания 15.1 и переделать ее таким образом, чтобы она возвращала словарь:
* ключ: имя интерфейса
* значение: кортеж с двумя строками:
  * IP-адрес
  * маска

В словарь добавлять только те интерфейсы, на которых настроены IP-адреса.

Например (взяты произвольные адреса):
{'FastEthernet0/1': ('10.0.1.1', '255.255.255.0'),
 'FastEthernet0/2': ('10.0.2.1', '255.255.255.0')}

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды, а не ввод пользователя.

"""


import re
from pprint import pprint

def get_ip_from_cfg(file):
    result = {}
    regex = (r'^interface (?P<iface>\S+)$'
             r'|ip address (?P<ipad_msk>\S+) (?P<ipmsk>\S+)')
    with open(file) as f:
        for line in f:
            s_match = re.search(regex,line)
            if s_match:
                #print(s_match)
                if s_match.lastgroup == 'iface':
                    interface = s_match.group(s_match.lastgroup)                    
                else:
                    result[interface] = (s_match.group('ipad_msk','ipmsk'))
    return result
    
pprint(get_ip_from_cfg('config_r1.txt'))
