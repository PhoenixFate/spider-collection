import time
import pymongo  # 引入pymongo模块


def save_detail_to_mongo(news_detail, tid):
    client = pymongo.MongoClient(host='114.67.89.253', port=40017)  # 进行连接
    db = client.feng  # 指定数据库
    db.authenticate("feng", "feng")
    collection = db.fengNewsDetail  # 指定集合
    try:
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        news_detail["createTime"] = create_time
        news_detail["tid"] = tid
        result = collection.find_one({'tid': tid})
        # print(result)
        # 不存在 则插入
        if result is None:
            print("insert one news detail")
            collection.insert(news_detail)
            # 查询新闻详情
    except Exception as e:
        print('新闻详情存储到MongoDb失败', e)
