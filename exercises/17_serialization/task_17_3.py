# -*- coding: utf-8 -*-
"""
Задание 17.3

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
"""

'SW1              Eth 0/0           140          S I      WS-C3750-  Eth 0/1'


import csv
import re
from pprint import pprint

regex = r'(\w+) +(\w+ [\d\/]+) +\d+ .+? +(\w+ [\d\/]+)'
def parse_sh_cdp_neighbors(sh_cdp):
    dev_name = re.search(r'(\S+)[>#]',sh_cdp).group(1)
    result = {dev_name:{}}
    match_list = re.findall(regex, sh_cdp)
    for match in match_list:
        a,b,c = match
        result[dev_name][b] = {a:c}
    return result



if __name__ == "__main__":
    with open("sh_cdp_n_r1.txt") as f:
        pprint(parse_sh_cdp_neighbors(f.read()))
