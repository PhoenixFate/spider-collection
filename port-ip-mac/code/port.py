from os import name
import threading
from socket import *
import tqdm  # 进度条，可自行加上

lock = threading.Lock()  # 确保 多个线程在共享资源的时候不会出现脏数据
openNum = 0  # 端口开放数量统计
threads = []  # 线程池


def portscanner(host, port):
    global openNum
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((host, port))
        lock.acquire()
        openNum += 1
        print(f"{port} open")
        lock.release()
        s.close()
    except:
        pass


def main(ip, ports=range(65535)):  # 设置 端口缺省值0-65535
    setdefaulttimeout(1)
    for port in ports:
        t = threading.Thread(target=portscanner, args=(ip, port))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print(f"PortScan is Finish ，OpenNum is {openNum}")


if __name__ == '__main__':
    ip = '221.226.135.114'
    ip2 = '221.226.96.98'
    # main(ip,[22,101,8080,8000])          # 输入端口扫描
    main(ip2)  # 全端口扫描