# -*- coding: utf-8 -*-
'''
Задание 5.3a

Дополнить скрипт из задания 5.3 таким образом, чтобы, в зависимости от выбранного режима,
задавались разные вопросы в запросе о номере VLANа или списка VLANов:
* для access: 'Введите номер VLAN:'
* для trunk: 'Введите разрешенные VLANы:'

Ограничение: Все задания надо выполнять используя только пройденные темы.
То есть эту задачу можно решить без использования условия if и циклов for/while.
'''

access_template = [
    'switchport mode access', 'switchport access vlan {}',
    'switchport nonegotiate', 'spanning-tree portfast',
    'spanning-tree bpduguard enable'
]

trunk_template = [
    'switchport trunk encapsulation dot1q', 'switchport mode trunk',
    'switchport trunk allowed vlan {}'
]

mode_in = input('Введите режим работы интерфейса (access/trunk): ')
interface_in = input('Введите тип и номер интерфейса: ')

vlans_question = {'access' : 'Введите номер влан: ',
'trunk' : 'Введите разрешенные VLANы: '}

ac_tr = {'access': access_template,
'trunk': trunk_template,}

vlans_in = input(vlans_question[mode_in])

print(('interface {}\n' + ('\n'.join(ac_tr[mode_in]))).format(interface_in,vlans_in))
