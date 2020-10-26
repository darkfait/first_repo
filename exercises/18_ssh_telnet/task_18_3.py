# -*- coding: utf-8 -*-
"""
Задание 18.3

Создать функцию send_commands (для подключения по SSH используется netmiko).

Параметры функции:
* device - словарь с параметрами подключения к одному устройству, которому надо передать команды
* show - одна команда show (строка)
* config - список с командами, которые надо выполнить в конфигурационном режиме

В зависимости от того, какой аргумент был передан, функция вызывает разные функции внутри.
При вызове функции send_commands, всегда будет передаваться только один из аргументов show, config.

Далее комбинация из аргумента и соответствующей функции:
* show - функция send_show_command из задания 19.1
* config - функция send_config_commands из задания 19.2

Функция возвращает строку с результатами выполнения команд или команды.

Проверить работу функции:
* со списком команд commands
* командой command

Пример работы функции:

In [14]: send_commands(r1, show='sh clock')
Out[14]: '*17:06:12.278 UTC Wed Mar 13 2019'

In [15]: send_commands(r1, config=['username user5 password pass5', 'username user6 password pass6'])
Out[15]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#username user5 password pass5\nR1(config)#username user6 password pass6\nR1(config)#end\nR1#'

"""

commands = ["logging 10.255.255.1", "logging buffered 20010", "no logging console"]
command = "sh ip int br"



import yaml
import re
from pprint import pprint
from netmiko import (ConnectHandler,
                    NetMikoAuthenticationException,
                    NetMikoTimeoutException)




def send_show_command(dev_add,command):
    try:
        with ConnectHandler(**dev_add) as ssh:
            ssh.enable()
            result = ssh.send_command(command)
        return result
    except (NetMikoAuthenticationException, NetMikoTimeoutException) as error:
        print(error)



#def send_config_commands(device,config_commands, log=True):
#    regex = (r'.+Invalid input detected.+?'
#             r'|.+Incomplete command.+?'
#             r'|.+Ambiguous command.+?')
#    if log:
#        log_print = f'Подключаюсь к {device["host"]}'
#        print(log_print)
#    with ConnectHandler(**device) as ssh:
#        result_correct = {}
#        result_errors = {}
#        ssh.enable()
#        for command in config_commands:
#            part_res = ssh.send_config_set(command)
#            match = re.search(regex,part_res)
#            if match:
#                print(f'Команда {command} выполнилась с ошибкой \"{match.group()}\"  на устройстве {device["host"]}')
#                result_errors[command] = part_res
#                if input('Продолжать выполнять команды? [y]/n :   ') in ('n','no'):
#                    break
#            else:
#                result_correct[command] = part_res
#        return (result_correct,result_errors)
    
def send_config_commands(device,config_commands):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        result = ssh.send_config_set(config_commands)
        return result
        

def send_commands(device,show=None,config=None):
    if show != None:
        result = send_show_command(device,show)
    elif config:
        #result_tup = send_config_commands(device,config)
        #result = '\n'.join(list(result_tup[0].values())) + ''.join(list(result_tup[1].values()))
        result = send_config_commands(device,config)
    return result


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    for dev in devices:
        pprint(send_commands(dev, config = commands))
