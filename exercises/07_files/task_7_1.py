# -*- coding: utf-8 -*-
'''
Задание 7.1

Аналогично заданию 4.6 обработать строки из файла ospf.txt
и вывести информацию по каждой в таком виде:
Protocol:              OSPF
Prefix:                10.0.24.0/24
AD/Metric:             110/41
Next-Hop:              10.0.13.3
Last update:           3d18h
Outbound Interface:    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''
#O        10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0
shabl = '''Protocol:              {d[0]:<10}
Prefix:                {d[1]:<10}
AD/Metric:             {d[2]:<10}
Next-Hop:              {d[3]:<10}
Last update:           {d[4]:<10}
Outbound Interface:    {d[5]:<10}\n'''

with open('ospf.txt') as source:
    for line in source:
        arg_list = line.replace('via','').replace('[','').replace(']','').replace('O','OSPF').split()
        print (shabl.format(d = arg_list))

        
