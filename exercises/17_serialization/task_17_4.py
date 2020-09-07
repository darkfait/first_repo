# -*- coding: utf-8 -*-
"""
Задание 17.4

Создать функцию write_last_log_to_csv.

Аргументы функции:
* source_log - имя файла в формате csv, из которого читаются данные (пример mail_log.csv)
* output - имя файла в формате csv, в который будет записан результат

Функция ничего не возвращает.

Функция write_last_log_to_csv обрабатывает csv файл mail_log.csv.
В файле mail_log.csv находятся логи изменения имени пользователя. При этом, email
пользователь менять не может, только имя.

Функция write_last_log_to_csv должна отбирать из файла mail_log.csv только
самые свежие записи для каждого пользователя и записывать их в другой csv файл.

Для части пользователей запись только одна и тогда в итоговый файл надо записать только ее.
Для некоторых пользователей есть несколько записей с разными именами.
Например пользователь с email c3po@gmail.com несколько раз менял имя:
C=3PO,c3po@gmail.com,16/12/2019 17:10
C3PO,c3po@gmail.com,16/12/2019 17:15
C-3PO,c3po@gmail.com,16/12/2019 17:24

Из этих трех записей, в итоговый файл должна быть записана только одна - самая свежая:
C-3PO,c3po@gmail.com,16/12/2019 17:24

Для сравнения дат удобно использовать объекты datetime из модуля datetime.
Чтобы упростить работу с датами, создана функция convert_datetimestr_to_datetime - она
конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
Полученные объекты datetime можно сравнивать между собой.

Функцию convert_datetimestr_to_datetime использовать не обязательно.

"""

import datetime
import csv


def convert_datetimestr_to_datetime(datetime_str):
    """
    Конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
    """
    return datetime.datetime.strptime(datetime_str, "%d/%m/%Y %H:%M")


def write_last_log_to_csv(source_log,output):
    with open(source_log) as f, open(output, 'w') as fo:
        result_dict = {}
        freader = csv.reader(f)
        writer = csv.writer(fo, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(next(freader))
        for row in freader:
            a,b,c = row
            if result_dict.get(b):
                date1 = convert_datetimestr_to_datetime(result_dict.get(b)[1])
                date2 = convert_datetimestr_to_datetime(c)
                if date2 > date1:
                    result_dict[b] = (a,c)
            else:
                result_dict[b] = (a,c)
        for key, val in result_dict.items():
            data = [val[0],key,val[1]]
            writer.writerow(data)
    return None

write_last_log_to_csv('mail_log.csv','test1.csv')

'''
def write_last_log_to_csv(source_log, output):
    with open(source_log) as f:
        data = list(csv.reader(f))
        header = data[0]
    result = {}
    sorted_by_date = sorted(
        data[1:], key=lambda x: convert_datetimestr_to_datetime(x[2])
    )
    for name, email, date in sorted_by_date:
        result[email] = (name, email, date)
    with open(output, "w") as dest:
        writer = csv.writer(dest)
        writer.writerow(header)
        for row in result.values():
            writer.writerow(row)
'''
