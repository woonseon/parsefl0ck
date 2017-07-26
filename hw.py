#-*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os
import time
from datetime import datetime, timedelta
import codecs
import pymysql

url = 'http://fl0ckfl0ck.info'
law = requests.get(url)
plain_text = law.text
soup = BeautifulSoup(plain_text, 'lxml')

link = soup.find_all("td")
link_k = soup.get_text("right")
#print(link_k)

editData = str(link_k)
editData = editData.replace('right', '')
editData = editData.replace('Apache/2.4.18 (Ubuntu) Server at fl0ckfl0ck.info Port 80', '')
editData = editData.replace('.zip', ' ')
editData = editData.replace('Index of /', '')
editData = editData.replace('NameLast modifiedSizeDescription', '')
editData_s = editData.split('\n')

del editData_s[0:9]
del editData_s[-5:-1]
del editData_s[-1]

#mysql connect
conn = pymysql.connect(host='127.0.0.1', user='root', password='apmsetup', db="capoo", charset="euckr")

count = 1

#print(list(editData_s[0])[0:5])
#print(editData_s) # editData 출력
temp_list = []
for i in editData_s:
    a = i.split(" ")
    a[1] = a[1] + " " + a[2]
    temp_list.append([a[0], a[1]])
    obj_datetime = datetime.strptime(a[1], '%Y-%m-%d %H:%M')
    #print("Num:%4d  IP: %15s  Date: %15s"%(count,a[0],obj_datetime))

    list_d = os.listdir('C:\\file')

    for j in list_d:
        if a[0] == j:
            file_name = 'C:\\file/%s\signCert.cert'%j
            f = codecs.open(file_name,'r','euckr')
            #f = open(file_name, 'r')
            line = f.readline()
            line = line.replace('cn=', '')
            line = line.replace('()', ',')
            line = line.replace('ou=', '')
            line = line.replace('o=', '')
            line = line.replace('c=', '')
            line_t = line.split(',')

            #print(line_t[0][-20:-1])
            #print(line_t)
            #print("Num:%5d  Date:%15s  Name:%s  Bank:%4s  Account:%20s  IP:%15s  Country:%7s"%(count,obj_datetime,line_t[0],line_t[2],line_t[1],a[0],line_t[5]))
            curs = conn.cursor()
            print(type(count))
            print(type(str(obj_datetime)))
            print(type(line_t[0]))
            print(type(a[0]))
            sql = "INSERT INTO info_db(count, date, name, bank, account, ip, country) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')"
            curs.execute(sql%(int(count), str(obj_datetime), line_t[0], line_t[2], line_t[1], a[0], line_t[5]))
            curs.close()
            f.close()
            count += 1
        else:
            continue
