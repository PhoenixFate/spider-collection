import math
import time
import requests
import json
from pprint import pprint
from aes import AESCipherCBC
from save_news import save_to_mongo
import schedule


def get_aes_code():
    # 威锋网的新闻数据的请求需要加密
    # 加密key  2b7e151628aed2a6
    # iv 偏移值 2b7e151628aed2a6
    e = AESCipherCBC(b'2b7e151628aed2a6', b'2b7e151628aed2a6')
    url2 = "/v1/content/list"
    data = "url=" + url2 + "$time=" + str(int(math.floor(time.time() * 1000))) + "000000"
    return e.encrypt(data)


def save_json(json_result):
    # 将json数据保存在当前目录文件news.json 便于查看返回的数据类型
    with open("news.json", "w", encoding="utf-8") as f:
        # json.dumps 能够把python类型转成json字符串
        # unicode字符串转成中文
        # indent  缩进
        f.write(json.dumps(json_result, ensure_ascii=False, indent=4))


def spider_news():
    session = requests.session()
    # 首页新闻数据
    feng_index_url = "https://beta-api.feng.com/v1/content/list?pageCount=20&page=1&isEnd=no"
    feng_data_url = "https://api.wfdata.club/v1/content/list?pageCount=20&page=2&isEnd="
    x_request_id = get_aes_code()
    headers = {
        "Origin": "https://www.feng.com",
        "Referer": "https://www.feng.com/",
        "X-Request-Id": x_request_id,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37"}
    response = session.get(url=feng_data_url, headers=headers)
    print(response.status_code)
    # json.loads 把字符串转成python类型
    json_result = json.loads(response.content.decode("utf-8"))
    print("获得数据成功！")
    # pretty print
    # pprint(json_result)
    # pprint(json_result["data"]["dataList"]["contentsList"])
    # 保存一份在本地文件
    save_json(json_result)
    # 保存新闻json对象到mongo
    save_to_mongo(json_result["data"]["dataList"]["contentsList"])


if __name__ == '__main__':
    print("spider of feng starts successfully")
    spider_news()
    # 每一个小时跑一次爬虫
    schedule.every(6).hours.do(spider_news)
    while True:
        schedule.run_pending()
