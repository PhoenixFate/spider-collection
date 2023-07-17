import time
import pymongo  # 引入pymongo模块


def save_to_mongo(data):
    client = pymongo.MongoClient(host='www.bytes-space.com', port=10717)  # 进行连接
    db = client.oa_advanced  # 指定数据库
    db.authenticate("oa", "centos123qwer")
    collection = db.almanac  # 指定集合
    try:
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        data["createTime"] = create_time
        result = collection.find_one({'id': data["id"]})
        # print(result)
        # 不存在 则插入
        if result is None:
            print("insert one data")
            collection.insert(data)
        else:
            print("该老黄历已经存在")

    except Exception as e:
        print('存储到MongoDb失败', e)
