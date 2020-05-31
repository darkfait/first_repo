# -*- coding: utf-8 -*-
'''
Задание 7.2b

Дополнить скрипт из задания 7.2a:
* вместо вывода на стандартный поток вывода,
  скрипт должен записать полученные строки в файл config_sw1_cleared.txt

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore.
Строки, которые начинаются на '!' отфильтровывать не нужно.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ignore = ['duplex', 'alias', 'Current configuration']

with open('config_sw1.txt') as conf_sw, open('config_sw1_cleared.txt', 'w') as conf_sw_cleared:
    for line in conf_sw:
        a1 = False
        for no_word in ignore:
            if no_word in line:
                a1 = True
                break
        if a1 == True:
            continue
        else:
            conf_sw_cleared.write(line.strip() + '\n')
            
