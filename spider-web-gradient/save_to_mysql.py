import pymysql

host = 'www.bytes-space.com'
port = 19306
user = 'root'
password = 'Common123qwer!@#'
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
    sql = "insert into gradient_color(title,image_url,css_code,colors) values(%s,%s,%s,%s)"
    for item in items:
        print(item)
        try:
            cursor.execute(sql, (item['title'], item['image_url'], item['css_code'], item['colors_string']))
        except Exception as e:
            print(e)
            return

    conn.commit()
    cursor.close()
    conn.close()
    print('sql执行成功')
