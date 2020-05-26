# -*- coding: utf-8 -*-
'''
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт:
Если адрес был введен неправильно, запросить адрес снова.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

ch_add = 0
while ch_add != 4:
    addr = input('введите IP-адрес в формате X.X.X.X:  ')
    addr_list = addr.split('.')
    try:
        for octet in addr_list:
            if int(octet) >= 0 and int(octet) <= 255 and len(addr_list) == 4:
                ch_add += 1
            else:
                print('Неправильный IP-адрес - октеты')
                break
        if ch_add == 4:
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
        continue



            

    

