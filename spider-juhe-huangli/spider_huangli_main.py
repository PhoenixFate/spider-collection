import math
import threading
import time
import requests
import json
from pprint import pprint
import schedule
import datetime
import time
from save_data import save_to_mongo
import pymongo  # 引入pymongo模块


def spider_huang_li(date):
    session = requests.session()
    # 首页新闻数据
    data_url = "https://www.juhe.cn/box/newtest"
    headers = {
        "authority": "www.juhe.cn",
        "method": "POST",
        "path": "/box/newtest",
        "scheme": "https",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6",
        "content-length": "71",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": "aliyungf_tc=dff37f92eb13283cf23ca49cf98c37ffc84c37b66fe224cc68584fcd3818e83c; acw_tc=2f6fc11716707687436363152e73c252954ef5d85aab99a69650419325e9d4; PHPSESSID=1aefa4sjoapcaepdsrjt34gtn4; hasReg=reged; _uuid_f1a125279935e03c3eea0c3c0d_v2=68a25fe00662c326393107ad99848265; JuheChannel=jHpassport-juhe-cn; _jhchle-68a25fe00662c326393107ad99848265=jHpassport-juhe-cn%2C1670768756%2C112.3.238.143%2CPC; __root_domain_v=.juhe.cn; _qddaz=QD.421270768756668; _qdda=3-1.1q5xsp; _qddab=3-qgq0ay.lbjgkvex; Hm_lvt_5d12e2b4eed3b554ae941c0ac43c330a=1670768757; PPA_CI=8c171a1cea678ee2f0d190e07dae514f; jh-dtaf4a8u96q0iiqsba9g8a=0; _refer_5e03c3eea0c3c0dubf1a12527993=https%3A//www.juhe.cn/docs/api/id/65; _local_5e03c3eea0c3c0dubf1a12527993=https%3A//www.juhe.cn/box/index/id/65; _f91834e654f46d9ed5afc3c0d=1875895ca4082f898ca065030e5b251f20e918015126FBf; Hm_lpvt_5d12e2b4eed3b554ae941c0ac43c330a=1670768791; XSRF-TOKEN=eyJpdiI6IkkzZmtIK1pnTWtza2tmV0d1MTRETWc9PSIsInZhbHVlIjoiRUxKdkIxNzRtSUs3am05SUJxdFRiZ1Vya25QTWloZHYrMzVrdVphc3MxeGhOM1hHVnNXVHdLTEN3OU9oZWI3Sk9uXC9mTktyZjArTkFXNWtNUDRmOThRPT0iLCJtYWMiOiJhMjA2OGJmMDUyZWU2MzY0ZGM4Y2JkM2IwNmYyM2E4MDExMzMwODMxMDg3ZjY1NjkyYzc5MjdlOTE4OTI4MmNiIn0%3D; juhe_cn_session=eyJpdiI6IlgyQTNJUDZBV2kxUm5MMkg4RDVmb2c9PSIsInZhbHVlIjoiOUtDS1pnZGo3dTBpWnBTZHpwOVlJZEJPdmRPMGFpaVkrVVwvczhiSmZxbkYxVVZsYVFrbVZOZWZrWlJvV3RLckhSMkxcL29ieFhjeFZyOGV5OXVKZGxzZz09IiwibWFjIjoiZThlMzI5NjU3NGNjZGU4NTZiM2NlYjQ3YWI5MjJlZDU0NDhkZTcyYTM3ZWFjYWRmOTRiOTc4YjJkZWIwNGVkZiJ9",
        "origin": "https://www.juhe.cn",
        "referer": "https://www.juhe.cn/box/index/id/65",
        "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "x-csrf-token": "FQtS1DeJwsRNh9mkFtkvnOAGY7ZJYsaTfmilhhEn",
        "x-requested-with": "XMLHttpRequest"}

    params = str('{"date": "abc"}').replace('abc', date)
    print(params)
    data = {
        "requesttypesel": "GET",
        "apiid": "174",
        "params": params
    }

    response = session.post(url=data_url, data=data, headers=headers)
    print(response.status_code)
    print(response.content)
    # json.loads 把字符串转成python类型
    json_result = json.loads(response.content.decode("utf-8"))
    print("获得数据成功！")
    # pretty print
    pprint(json_result)
    pprint(json_result['result']['response'])
    response_text = str(json_result['result']['response'])
    final_result = response_text.replace('\t', '').replace('\r\n', '').replace('&quot;', '"')
    pprint(json.loads(final_result)['result'])
    # 保存一份在本地文件
    # 保存新闻json对象到mongo
    save_to_mongo(json.loads(final_result)['result'])


def job_spider_huang_li():
    threading.Thread(target=spider_huang_li, args=['2022-12-13']).start()


def test_date():
    # 查询库里面的最后一条记录的时间
    client = pymongo.MongoClient(host='www.bytes-space.com', port=10717)  # 进行连接
    db = client.oa_advanced  # 指定数据库
    db.authenticate("oa", "centos123qwer")
    collection = db.almanac  # 指定集合
    # sort("name", 1)  # 顺序
    # sort("name", -1)  # 倒序
    data_list = collection.find().sort("yangli", -1)
    # for one in data_list:
    #     print(one)
    first = data_list[0]
    print(first)
    print(first['yangli'])
    begin_date = datetime.datetime.strptime(first['yangli'], "%Y-%m-%d")
    print(begin_date)
    end_date = (begin_date + datetime.timedelta(days=49)).strftime("%Y-%m-%d")
    print(end_date)
    date_list = []
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        # time.sleep(3)
        spider_huang_li(date_str)
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    print(date_list)


if __name__ == '__main__':
    print("spider of juhe starts successfully")
    # job_spider_huang_li()
    test_date()
