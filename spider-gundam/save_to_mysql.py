import pymysql

host = 'www.bytes-space.com'
port = 41306
user = 'root'
password = 'centos123qwer'
db = 'spider_collection'


# 打开数据库连接，不指定数据库
# ---- 用pymysql 操作数据库
def get_connection():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, password=password)
    return conn


def save_items(items):
    print(items)
    conn = get_connection()
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = conn.cursor()
    # 另一种插入数据的方式，通过字符串传入值
    sql = "insert into gundam(gundam_name,gundam_image,gundam_type) values(%s,%s,%s)"
    for item in items:
        print(item)
        try:
            cursor.execute(sql, (item['name'], item['image'], item['type']))
        except Exception as e:
            print(e)
            return

    conn.commit()
    cursor.close()
    conn.close()
    print('sql执行成功')
