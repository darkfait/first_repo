# -*- coding: utf-8 -*-

    
import sqlite3
import os
import re
import yaml
import sys
from pprint import pprint
from datetime import timedelta, datetime



#Блок проверки наличия файла
def file_check(file_name):
    file_exist = os.path.exists(file_name)
    return file_exist

def create_db(db_file_name, db_schema):
    if not file_check(db_file_name):
        print('Creating database...')
        conn = sqlite3.connect(db_file_name)
        with open(db_schema, 'r') as f:
            schema = f.read()
            conn.executescript(schema)
        print('Database created')
        conn.close()
    else:
        print('Such file already exist')
    


#Add data to sitches-db

def list_data_switches(switches_data_file):
    for sw_file in switches_data_file:
        with open(sw_file) as f:
            sw_data = yaml.safe_load(f)['switches']
            data_switches = []
            for sw_hostname, sw_values in sw_data.items():
                data_switches.append((sw_hostname, sw_values))
    return(data_switches)

def add_data_switches_func(connect,switches_file):
    print('Добавляю данные в таблицу switches...')
    for sw_data in list_data_switches(switches_file):
        try:
            with connect:
                query_sw = "INSERT into switches values (?, ?)"
                connect.execute(query_sw,sw_data)
        except sqlite3.IntegrityError as err:
            print('При добавлении данных: ', sw_data, 'Возникла ошибка: ', err)
    return

def add_data_switches(db_file_name, data_file_name):
    if not file_check(db_file_name):
        print('База данных не существует. Перед добавлением данных, ее надо создать')
    else:
        connect = sqlite3.connect(db_file_name)
        #ADD DATA TO SWITCHES TABLE
        add_data_switches_func(connect,data_file_name)
        connect.close()


#Add data to DHCP-db

def list_data_dhcp(dhcp_fname):
    sw_name = dhcp_fname[dhcp_fname.find('sw'):dhcp_fname.find('_dhcp')]
    regex_data = r'([\w:]+) +([\d.]+).+? dhcp-snooping +(\d+) +(\S+)'
    with open(dhcp_fname) as f:
        match_iter = re.finditer(regex_data,f.read())
        values_list = []
        for match in match_iter:
            mac,ip,vlan,iface = match.groups()
            values_list.append([mac, ip, vlan, iface, sw_name])
    return(values_list)

def delete_old_data(connect):
    #connect = sqlite3.connect(db_file)
    now = datetime.today().replace(microsecond=0)
    week_ago = now - timedelta(days=7)
    query_delet_old = "DELETE from dhcp where last_active < ?"
    connect.execute(query_delet_old,(str(week_ago),))
    connect.commit()
    #connect.close()
    return

def add_data_dhcp_func(connect,dhcp_files_list):
    print('Добавляю данные в таблицу dhcp...')
    query_10 = "UPDATE dhcp set active = '0'"
    connect.execute(query_10)
    delete_old_data(connect)
    connect.commit()
    for dhcp_file in dhcp_files_list:
        for dhcp_data in list_data_dhcp(dhcp_file):
            try:
                with connect:
                    query_dhcp = "INSERT into dhcp values (?, ?, ?, ?, ?, 1,datetime('now'))"
                    connect.execute(query_dhcp,dhcp_data)
            except sqlite3.IntegrityError as err:
                with connect:
                    query_dhcp = "REPLACE into dhcp values (?, ?, ?, ?, ?, 1,datetime('now'))"
                    connect.execute(query_dhcp,dhcp_data)
    return

def add_data(db_file, filename):
    if not file_check(db_file):
        print('База данных не существует. Перед добавлением данных, ее надо создать')
    else:
        #ADD DATA TO DHCP TABLE
        connect = sqlite3.connect(db_file)
        add_data_dhcp_func(connect,filename)
        connect.close()

    

#GET DATA Script

def get_data(file_db, key, val):
    db_keys = ('mac', 'ip', 'vlan', 'interface', 'switch', 'active')
    if key not in db_keys:
        print('Данный параметр не поддерживается.\nДопустимые значения параметров: mac, ip, vlan, interface, switch, active')
    else:
        connect = sqlite3.connect(file_db)
        query_kv = 'SELECT * from dhcp WHERE {} = ? AND active = {}'
        result_act = connect.execute(query_kv.format(key,"1"),(val,))
        result_pass = connect.execute(query_kv.format(key,"0"),(val,))
        print('Активные записи:\n','-' * 70)
        for row in result_act:
            print(row)
        if result_pass.fetchmany(1):
            result_pass = connect.execute(query_kv.format(key,"0"),(val,))
            print('\nНеактивные записи:\n','-' * 70)
            for row in result_pass:
                print(row)
    return([result_act,result_pass])

def get_all_data(file_db):
    query_all = 'SELECT * from dhcp WHERE active = {}'
    connect = sqlite3.connect(file_db)
    result_act = connect.execute(query_all.format("1"))
    result_pass = connect.execute(query_all.format("0"))
    print('Активные записи:\n','-' * 70)
    for row in result_act:
        print(row)
    if result_pass.fetchmany(1):
        result_pass = connect.execute(query_all.format("0"))
        print('\nНеактивные записи:\n','-' * 70)
        for row in result_pass:
            print(row)
    return([result_act,result_pass])
    

