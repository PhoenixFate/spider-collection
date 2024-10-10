import pymysql
from MySQLConnectionPool import MySQLConnectionPool

host = '172.16.1.219'
port = 3306
user = 'root'
password = '123456789'
db = 'fdc'
mysql_pool = MySQLConnectionPool("dev")


def save_shop_rental_item(item):
    # 先查询，如果存在则更新
    query_one_sql = "select * from shop_rental where id=%s"
    old_data = mysql_pool.select_one(query_one_sql, item['house_id'])
    if old_data is None:
        insert_sql = "insert into shop_rental(id,shop_name,shop_address,price,price_short,price_str,price_unit,price_daily,area,lat,lng,street,region) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        mysql_pool.insert_one(insert_sql,
                              (item['house_id'],
                               item['title'],
                               item['address'],
                               item['price'],
                               item['price_short'],
                               item['price_str'],
                               item['price_unit'],
                               item['price_daily'],
                               item['area'],
                               item['lat'],
                               item['lng'],
                               item['street'],
                               item['region']
                               ))
        print('新增成功')
    else:
        update_sql = "update shop_rental set shop_name=%s,shop_address=%s,price=%s,price_short=%s,price_str=%s,price_unit=%s,price_daily =%s,area =%s,lat =%s,lng =%s,street =%s,region =%s where id=%s"
        mysql_pool.update_one(update_sql,
                              (
                                  item['title'],
                                  item['address'],
                                  item['price'],
                                  item['price_short'],
                                  item['price_str'],
                                  item['price_unit'],
                                  item['price_daily'],
                                  item['area'],
                                  item['lat'],
                                  item['lng'],
                                  item['street'],
                                  item['region'],
                                  item['house_id']
                              ))
        print('修改成功')


def save_shop_sell_item(item):
    # 先查询，如果存在则更新
    query_one_sql = "select * from shop_sell where id=%s"
    old_data = mysql_pool.select_one(query_one_sql, item['house_id'])
    if old_data is None:
        insert_sql = "insert into shop_sell(id,shop_name,shop_address,price,price_short,price_str,price_unit,price_total,area,lat,lng,street,region) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        mysql_pool.insert_one(insert_sql,
                              (item['house_id'],
                               item['title'],
                               item['address'],
                               item['price'],
                               item['price_short'],
                               item['price_str'],
                               item['price_unit'],
                               item['price_total'],
                               item['area'],
                               item['lat'],
                               item['lng'],
                               item['street'],
                               item['region']
                               ))
        print('新增成功')
    else:
        update_sql = "update shop_sell set shop_name=%s,shop_address=%s,price=%s,price_short=%s,price_str=%s,price_unit=%s,price_total =%s,area =%s,lat =%s,lng =%s,street =%s,region =%s where id=%s"
        mysql_pool.update_one(update_sql,
                              (
                                  item['title'],
                                  item['address'],
                                  item['price'],
                                  item['price_short'],
                                  item['price_str'],
                                  item['price_unit'],
                                  item['price_total'],
                                  item['area'],
                                  item['lat'],
                                  item['lng'],
                                  item['street'],
                                  item['region'],
                                  item['house_id']
                              ))
        print('修改成功')
