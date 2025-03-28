from MySQLConnectionPool import MySQLConnectionPool
from snow import IdWorker


class DataSource:
    def __init__(self, environment):
        self.environment = environment
        self.mysql_pool = MySQLConnectionPool(environment)
        self.worker = IdWorker(1, 2, 0)

    def delete_item(self, item):
        delete_sql = "delete from item where id=%s"
        self.mysql_pool.delete_one(delete_sql, str(item['id']))
        print('删除成功')

    def save_item(self, item):
        print(item)
        # 先查询，如果存在则更新
        query_one_sql = "select * from item where item_id=%s"
        old_data = self.mysql_pool.select_one(query_one_sql, str(item['item_id']))
        if old_data is None:
            big_id = str(self.worker.get_id())
            insert_sql = (
                "insert into item(id,item_id,tag,cover_url,cover_origin_url,title,category,big_category,size,introduction,has_source) "
                "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            self.mysql_pool.insert_one(insert_sql,
                                       (big_id, str(item['item_id']), item['tag'], item['cover_url'],
                                        item['cover_origin_url'],
                                        item['title'], item['category'],
                                        item['big_category'],
                                        item['size'], item['introduction'], item['has_source']))
            print('新增成功')
        else:
            update_sql = "update item set item_id=%s,tag=%s,cover_url=%s,cover_origin_url=%s, title=%s,category=%s,big_category=%s,size =%s,introduction =%s,has_source =%s where id=%s"
            self.mysql_pool.update_one(update_sql,
                                       (str(item['item_id']), item['tag'], item['cover_url'], item['cover_origin_url'],
                                        item['title'],
                                        item['category'], item['big_category'], item['size'], item['introduction'],
                                        item['has_source'],
                                        old_data['id']))
            print('修改成功')
