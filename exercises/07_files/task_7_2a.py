# -*- coding: utf-8 -*-
'''
Задание 7.2a

Сделать копию скрипта задания 7.2.

Дополнить скрипт:
  Скрипт не должен выводить команды, в которых содержатся слова,
  которые указаны в списке ignore.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ignore = ['duplex', 'alias', 'Current configuration']



with open('config_sw1.txt') as conf_sw:
    for line in conf_sw:
        a1 = False
        if line.startswith('!'):
            continue
        for no_word in ignore:
            if no_word in line:
                a1 = True
                break
        if a1 == True:
            continue
        else:
            print(line.strip())
            
