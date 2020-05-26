# -*- coding: utf-8 -*-
'''
Задание 6.2

1. Запросить у пользователя ввод IP-адреса в формате 10.0.1.1
2. Определить тип IP-адреса.
3. В зависимости от типа адреса, вывести на стандартный поток вывода:
   'unicast' - если первый байт в диапазоне 1-223
   'multicast' - если первый байт в диапазоне 224-239
   'local broadcast' - если IP-адрес равен 255.255.255.255
   'unassigned' - если IP-адрес равен 0.0.0.0
   'unused' - во всех остальных случаях


Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

addr = input('введите IP-адрес в формате X.X.X.X:  ')
addr_num_0 = int(addr.split('.')[0])
if addr_num_0 > 0 and addr_num_0 < 224:
    print('unicast')
elif addr_num_0 > 223 and addr_num_0 < 240:
    print('multicast')
elif addr == '255.255.255.255':
    print('local broadcast')
elif addr == '0.0.0.0':
    print('unassigned')
else:
    print('unused')
