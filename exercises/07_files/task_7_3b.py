# -*- coding: utf-8 -*-
'''
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Дополнить скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

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
    input_vlan = input('Введите номер Vlan:   ')
    for line in sorted_new_cam_list:
        if line[0] == input_vlan:
            print('{:<10}   {:<10}  {:<10}'.format(line[0],line[1],line[2]))
            
