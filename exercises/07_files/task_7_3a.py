# -*- coding: utf-8 -*-
'''
Задание 7.3a

Сделать копию скрипта задания 7.3.

Дополнить скрипт:
- Отсортировать вывод по номеру VLAN

В результате должен получиться такой вывод:
10       01ab.c5d0.70d0      Gi0/8
10       0a1b.1c80.7000      Gi0/4
100      01bb.c580.7000      Gi0/1
200      0a4b.c380.7c00      Gi0/2
200      1a4b.c580.7000      Gi0/6
300      0a1b.5c80.70f0      Gi0/7
300      a2ab.c5a0.700e      Gi0/3
500      02b1.3c80.7b00      Gi0/5
1000     0a4b.c380.7d00      Gi0/9


Ограничение: Все задания надо выполнять используя только пройденные темы.

'''



with open('CAM_table.txt') as cam_table:
    new_cam_list = []
    sorted_new_cam_list = []
    sncl_1 = []
    sncl_2 = []
    sncl_3 = []
    sncl_4 = []
    for line in cam_table:
        if line.count('.') != 2:
            continue
        else:
            new_cam_list.append(line.replace('    DYNAMIC     ','   ').strip().split())
    for mac_line in sorted(new_cam_list):
        if int(mac_line[0]) < 10:
            sncl_1.append(mac_line)
    for mac_line in sorted(new_cam_list):
        if int(mac_line[0]) < 100 and int(mac_line[0]) >= 10:
            sncl_1.append(mac_line)
    for mac_line in sorted(new_cam_list):
        if int(mac_line[0]) < 1000 and int(mac_line[0]) >= 100:
            sncl_1.append(mac_line)
    for mac_line in sorted(new_cam_list):
        if int(mac_line[0]) < 10000 and int(mac_line[0]) >= 1000:
            sncl_1.append(mac_line)
    sorted_new_cam_list = sncl_1 + sncl_2 + sncl_3 + sncl_4
    for line in sorted_new_cam_list:
        print('{:<10}   {:<10}  {:<10}'.format(line[0],line[1],line[2]))
            
                
