# -*- coding: utf-8 -*-
'''
Код в скриптах должен быть разбит на функции. 
Какие именно функции и как разделить код, надо решить самостоятельно. 
Часть кода может быть глобальной.

1. create_db.py - в этот скрипт должна быть вынесена функциональность по созданию БД:
  * должна выполняться проверка наличия файла БД
  * если файла нет, согласно описанию схемы БД в файле dhcp_snooping_schema.sql, должна быть создана БД
  * имя файла бд - dhcp_snooping.db

В БД должно быть две таблицы (схема описана в файле dhcp_snooping_schema.sql):
 * switches - в ней находятся данные о коммутаторах
 * dhcp - тут хранится информация полученная из вывода sh ip dhcp snooping binding

Пример выполнения скрипта, когда файла dhcp_snooping.db нет:
$ python create_db.py
Создаю базу данных...

После создания файла:
$ python create_db.py
База данных существует

!!!!      -- Schema for dhcp-snopping parsing example.
!!!!      
!!!!      create table switches (
!!!!          hostname    text not null primary key,
!!!!          location    text
!!!!      );
!!!!      
!!!!      create table dhcp (
!!!!          mac          text primary key,
!!!!          ip           text,
!!!!          vlan         text,
!!!!          interface    text,
!!!!          switch       text not null references switches(hostname)
!!!!      );
          
'''

import sqlite3
import os



my_db_file_name = 'dhcp_snooping.db'
dhcp_db_chema = 'dhcp_snooping_schema.sql'

def file_check(file_name):
    file_exist = os.path.exists(file_name)
    return file_exist


def create_db(db_file_name, schema_file):
    print('Creating database...')
    conn = sqlite3.connect(db_file_name)
    with open(schema_file, 'r') as f:
        schema = f.read()
        conn.executescript(schema)
    print('Database created')
    conn.close()
    


if __name__ == "__main__":
    if not file_check(my_db_file_name):
        create_db(my_db_file_name, dhcp_db_chema)
    else:
        print('Such file already exist')

