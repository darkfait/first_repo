# -*- coding: utf-8 -*-
'''
Задание 4.7

Преобразовать MAC-адрес mac в двоичную строку такого вида:
'101010101010101010111011101110111100110011001100'

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

mac = 'AAAA:BBBB:CCCC'

(str(bin(int(mac[:4],16)))+str(bin(int(mac[5:9],16)))+str(bin(int(mac[10:14],16)))).replace('0b','') 


mac_part = mac.split(':')
(str(bin(int(mac_part[0],16)))+str(bin(int(mac_part[1],16)))+str(bin(int(mac_part[2],16)))).replace('0b','') 
