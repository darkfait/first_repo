# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""


from concurrent.futures import ThreadPoolExecutor
import logging 
import subprocess
from pprint import pprint


logging.basicConfig(
    format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)
    

def ping_one(ipadd):
    start_msg = '===> Perform ping command for address {}'.format(ipadd)
    logging.info(start_msg)
    test = subprocess.run(['ping','-c', '3','-n', ipadd],stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding = 'UTF-8')
    #result = test.stdout.decode('utf-8')
    return test

def ping_ip_addresses(ip_adds):
    fine_adds = []
    bad_adds = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        result = executor.map(ping_one,ip_adds)
    for ip,res in zip(ip_adds,result):
        if res.returncode == 0:
            fine_adds.append(ip)
        else:
            bad_adds.append(ip)
    return (fine_adds,bad_adds)

#192.168.100.1

#print(ping_one('192.168.100.1'))
if __name__ == "__main__":
    my_ip_ads = ['192.168.100.1','192.168.100.2','192.168.100.30']
    pprint(ping_ip_addresses(my_ip_ads))
