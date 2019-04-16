# -*- coding: utf-8 -*-

import subprocess
import re


def get_ping_result(ip_address):
    p = subprocess.Popen(["ping.exe", ip_address], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True)
    out = p.stdout.read().decode('gbk')
    print(out)

    reg_receive = '已接收 = \d'
    match_receive = re.search(reg_receive, out)

    receive_count = -1

    if match_receive:
        receive_count = int(match_receive.group()[6:])

    if receive_count > 0:  # 接受到的反馈大于0，表示网络通
        reg_min_time = '最短 = \d+ms'
        reg_max_time = '最长 = \d+ms'
        reg_avg_time = '平均 = \d+ms'
        reg_lose_cout     = '丢失 = \d'

        match_min_time = re.search(reg_min_time, out)
        min_time = int(match_min_time.group()[5:-2])

        match_max_time = re.search(reg_max_time, out)
        max_time = int(match_max_time.group()[5:-2])

        match_avg_time = re.search(reg_avg_time, out)
        avg_time = int(match_avg_time.group()[5:-2])

        match_lose_count = re.search(reg_lose_cout, out)
        lose_count = int(match_lose_count.group()[5:])

        return lose_count
    else:
        print('网络不通，目标服务器不可达！')
        return 9999
def send_message(count):
    print(count)

if __name__ == '__main__':
    ping_result = get_ping_result('106.75.94.62')
    print(ping_result)
    if(ping_result > 0):
        send_message()