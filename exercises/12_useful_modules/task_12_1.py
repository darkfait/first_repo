# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

import subprocess

def ping_ip_addresses(ip_list):
    print('work in progress')
    alive = []
    lost = []
    for ip_adr in ip_list:
        if subprocess.run(['ping','-c','1', ip_adr],stdout=subprocess.DEVNULL).returncode == 0:
            alive.append(ip_adr)
        else:
            lost.append(ip_adr)
    result = (alive, lost)
    return result
    

if __name__ == "__main__":
    ipadds= [
        "8.8.8.8",
        "9.9.9.9",
        "10.0.0.1"]
    print(ping_ip_addresses(ipadds))
