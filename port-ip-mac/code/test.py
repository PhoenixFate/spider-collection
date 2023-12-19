# -*- coding: utf-8 -*-

import os
import platform
import socket
import threading
import time
import re
from scapy.all import *
import socket

from scapy.layers.l2 import ARP, Ether

live_ip = 0


def get_os():
    os = platform.system()
    if os == "Windows":
        return "n"
    else:
        return "c"


def ping_ip(ip_str):
    cmd = ["ping", "-{op}".format(op=get_os()),
           "1", ip_str]
    output = os.popen(" ".join(cmd)).readlines()
    for line in output:
        if str(line).upper().find("TTL") >= 0:
            HOSTNAME2 = socket.getfqdn(ip_str)
            g = IP2MAC()
            print("ip: %s 在线  计算机名为：%s   MAC地址: %s mac2: %s" % (ip_str, HOSTNAME2, g.getMac(ip_str)))

            # print(" 计算机名为：", HOSTNAME2)
            global live_ip
            live_ip += 1
            break


def find_ip(ip_prefix):
    '''''
    给出当前的ip地址段 ，然后扫描整个段所有地址
    '''
    threads = []
    for i in range(1, 256):
        ip = '%s.%s' % (ip_prefix, i)
        # ping_ip(ip)
        threads.append(threading.Thread(target=ping_ip, args={ip, }))
    for i in threads:
        i.start()
    for i in threads:
        i.join()


def find_local_ip():
    """
    获取本机当前ip地址
    :return: 返回本机ip地址
    """
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    return myaddr

class IP2MAC:
    """
    Python3根据IP地址获取MAC地址（不能获取本机IP，可以获取与本机同局域网设备IP的MAC）
    """

    def __init__(self):
        self.patt_mac = re.compile('([a-f0-9]{2}[-:]){5}[a-f0-9]{2}', re.I)

    def getMac(self, ip):
        sysstr = platform.system()

        if sysstr == 'Windows':
            macaddr = self.__forWin(ip)
        elif sysstr == 'Linux':
            macaddr = self.__forLinux(ip)
        else:
            macaddr = None

        return macaddr or '00-00-00-00-00-00'

    def __forWin(self, ip):
        os.popen('ping -n 1 -w 500 {} > nul'.format(ip))
        macaddr = os.popen('arp -a {}'.format(ip))
        macaddr = self.patt_mac.search(macaddr.read())

        if macaddr:
            macaddr = macaddr.group()
        else:
            macaddr = None

        return macaddr

    def __forLinux(self, ip):
        os.popen('ping -nq -c 1 -W 500 {} > /dev/null'.format(ip))

        result = os.popen('arp -an {}'.format(ip))

        result = self.patt_mac.search(result.read())

        return result.group() if result else None


if __name__ == "__main__":
    print("开始扫描时间: %s" % time.ctime())
    addr = find_local_ip()
    print(addr)
    args = "".join(addr)
    ip_pre = '.'.join(args.split('.')[:-1])
    print(ip_pre)
    find_ip("172.16.0")
    find_ip("172.16.1")
    find_ip("172.16.2")
    find_ip("172.16.3")
    find_ip("172.16.4")
    print("扫描结束时间 %s" % time.ctime())
    print('本次扫描共检测到本网络存在%s台设备' % live_ip)
