from includee import *
import sql_union_attack
import sql_blind_time_attack
import sql_error_attack
import sql_blind_bool_attack
from colorama import init

if __name__ == "__main__":
    init(autoreset=True)
    url = input('请输入url:')
    cookie = input('请输入cookies信息:')
    print("\033[1;31m*\033[0m" * 50)
    print("请选择:")
    print("[1]布尔盲注")
    print("[2]时间盲注")
    print("[3]报错注入")
    print("[4]联合查询注入")
    print("\033[1;31m*\033[0m" * 50)
    in_num = input('输入数字选择注入类型')
    print("\033[1;31m[INFO]\033[0m 正在进行SQL注入")
    if int(in_num) == 1:
        headers, ip = get_header(url, cookie)
        sql_blind_bool_attack.sql_blind_attack(url, headers)
    elif int(in_num) == 2:
        headers, ip = get_header(url, cookie)
        sql_blind_time_attack.sql_time_attack(url,headers)
    elif int(in_num) == 3:
        headers, ip = get_header(url, cookie)
        sql_error_attack.sql_error_attack(url, headers)
    elif int(in_num) == 4:
        headers, ip = get_header(url, cookie)
        sql_union_attack.sql_union_attack(url,headers)
    else:
        quit()