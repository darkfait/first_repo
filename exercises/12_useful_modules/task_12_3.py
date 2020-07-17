# -*- coding: utf-8 -*-
"""
Задание 12.3


Создать функцию print_ip_table, которая отображает таблицу доступных и недоступных IP-адресов.

Функция ожидает как аргументы два списка:
* список доступных IP-адресов
* список недоступных IP-адресов

Результат работы функции - вывод на стандартный поток вывода таблицы вида:

Reachable    Unreachable
-----------  -------------
10.1.1.1     10.1.1.7
10.1.1.2     10.1.1.8
             10.1.1.9

Функция не должна изменять списки, которые переданы ей как аргументы.
То есть, до выполнения функции и после списки должны выглядеть одинаково.


Для этого задания нет тестов
"""

from tabulate import tabulate

def print_ip_table(reach_list, unreach_list):
    columns = ['Reachable','Unreachable']
    print(tabulate([reach_list,unreach_list], headers = columns))
    return reach_list, unreach_list

if __name__ == "__main__":
    rea = ['1.1.1.1','2.2.2.2']
    unrea = ['3.3.3.3']
    print_ip_table(rea,unrea)

