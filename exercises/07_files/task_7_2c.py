# -*- coding: utf-8 -*-
'''
Задание 7.2c

Переделать скрипт из задания 7.2b:
* передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

Внутри, скрипт должен отфильтровать те строки, в исходном файле конфигурации,
в которых содержатся слова из списка ignore.
И записать остальные строки в итоговый файл.

Проверить работу скрипта на примере файла config_sw1.txt.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

from sys import argv

ignore = ['duplex', 'alias', 'Current configuration']

with open(argv[1]) as conf_sw, open(argv[2], 'w') as conf_sw_cleared:
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
     
