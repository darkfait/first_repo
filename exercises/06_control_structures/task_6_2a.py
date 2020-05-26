# -*- coding: utf-8 -*-
'''
Задание 6.2a

Сделать копию скрипта задания 6.2.

Добавить проверку введенного IP-адреса. Адрес считается корректно заданным, если он:
   - состоит из 4 чисел разделенных точкой,
   - каждое число в диапазоне от 0 до 255.

Если адрес задан неправильно, выводить сообщение:
'Неправильный IP-адрес'

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''
ch_add = False
try:
    addr = input('введите IP-адрес в формате X.X.X.X:  ')
    addr_list = addr.split('.')
    for octet in addr_list:
        if int(octet) >= 0 and int(octet) <= 255 and len(addr_list) == 4:
            ch_add = True
        else:
            print('Неправильный IP-адрес - октеты')
            break
    if ch_add == True:
        addr_num_0 = int(addr_list[0])
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
    
except ValueError:
    print('Неправильный IP-адрес - буквы')


#ch_add = False
#try:
#    while ch_add == False:
#        addr = input('введите IP-адрес в формате X.X.X.X:  ')
#        addr_list = addr.split('.')
#        for octet in addr_list:
#            if len(addr_list) == 4 and int(octet) >= 0 and int(octet) <= 255:
#                ch_add = True
#            else:
#                print('Неправильный IP-адрес')
#                break
#except ValueError:
#    print('Неправильный IP-адрес')
#
#
#addr_num_0 = int(addr.split('.')[0])
#if addr_num_0 > 0 and addr_num_0 < 224:
#    print('unicast')
#elif addr_num_0 > 223 and addr_num_0 < 240:
#    print('multicast')
#elif addr == '255.255.255.255':
#    print('local broadcast')
#elif addr == '0.0.0.0':
#    print('unassigned')
#else:
#    print('unused')
