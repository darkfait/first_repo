# -*- coding: utf-8 -*-
'''
Задание 4.6

Обработать строку ospf_route и вывести информацию на стандартный поток вывода в виде:
Protocol:              OSPF
Prefix:                10.0.24.0/24
AD/Metric:             110/41
Next-Hop:              10.0.13.3
Last update:           3d18h
Outbound Interface:    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ospf_route = 'O        10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0'



ospf_list = ospf_route.replace(',',' ').replace('O    ','OSPF').replace('via','').split()

a0 = ospf_list[0]
a1 = ospf_list[1]
a2 = ospf_list[2]
a3 = ospf_list[3]
a4 = ospf_list[4]
a5 = ospf_list[5]

t_ospf_route = '''
    Protocol:              {:<} 
    Prefix:                {:<} 
    AD/Metric:             {:<} 
    Next-Hop:              {:<} 
    Last update:           {:<} 
    Outbound Interface:    {:<}'''  



'''
!ВТОРОЙ ВАРИАНТ!

ospf_list = ospf_route.replace(',',' ').replace('O    ','OSPF').replace('via','').split()

t_ospf_route = '''
    Protocol:              {d[0]:<} 
    Prefix:                {d[1]:<} 
    AD/Metric:             {d[2]:<} 
    Next-Hop:              {d[3]:<} 
    Last update:           {d[4]:<} 
    Outbound Interface:    {d[5]:<}'''  

print(t_ospf_route.format(d=ospf_list)) 

'''
