import time
import pymongo  # 引入pymongo模块
from spider_news_detail import spider_detail_news


def save_to_mongo(news_array):
    client = pymongo.MongoClient(host='114.67.89.253', port=40017)  # 进行连接
    db = client.feng  # 指定数据库
    db.authenticate("feng", "feng")
    collection = db.fengNews  # 指定集合
    try:
        for news in news_array:
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            news["createTime"] = create_time
            result = collection.find_one({'tid': news["tid"]})
            # print(result)
            # 不存在 则插入
            if result is None:
                print("insert one news")
                collection.insert(news)
                # 查询新闻详情
                spider_detail_news(news["tid"])

    except Exception as e:
        print('存储到MongoDb失败', e)
