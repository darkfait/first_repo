import sys

# -*- coding: utf-8 -*-
'''
Задание 5.2b

Преобразовать скрипт из задания 5.2a таким образом,
чтобы сеть/маска не запрашивались у пользователя,
а передавались как аргумент скрипту.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''


#ip_in = input('Введите ip-сеть в формате xx.xx.xx.xx/xx:  ')
#ip_in = '10.1.1.0/24'
ip_in = sys.argv[1]
net_in = ip_in[:ip_in.find('/')].split('.')

mask_in = ip_in[ip_in.find('/')+1:]
mask_bin_full = int(mask_in)*'1' + (32 - int(mask_in))*'0'
mask_int = [int(mask_bin_full[0:8],2), int(mask_bin_full[8:16],2), int(mask_bin_full[16:24],2), int(mask_bin_full[24:32],2)]

net_int = [(int(net_in[0]) & mask_int[0]), (int(net_in[1]) & mask_int[1]), (int(net_in[2]) & mask_int[2]), (int(net_in[3]) & mask_int[3])]


info ='''
Network:
{a[0]:<10}{a[1]:<10}{a[2]:<10}{a[3]:<10}
{a[0]:<08b}  {a[1]:<08b}  {a[2]:<08b}  {a[3]:<08b}  

Mask:
{c:<10}
{b[0]:<10}{b[1]:<10}{b[2]:<10}{b[3]:<10}
{b[0]:<08b}  {b[1]:<08b}  {b[2]:<08b}  {b[3]:<08b}  
'''

print(info.format(a = net_int, b =mask_int, c = mask_in))
