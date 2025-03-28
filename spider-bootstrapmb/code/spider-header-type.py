import sys

import pymysql
import requests
from bs4 import BeautifulSoup

from MySQLConnectionPool import MySQLConnectionPool
from snow import IdWorker


def get_connection(host, port, db, user, password):
    conn = pymysql.connect(host=host, port=port, db=db, user=user, password=password)
    return conn


class GetWeather:
    def __init__(self, environment):
        self.environment = environment
        self.base_url = r"https://www.bootstrapmb.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37"}
        self.mysql_pool = MySQLConnectionPool(environment)
        self.worker = IdWorker(1, 2, 0)
        print(self.mysql_pool)

    def _get_header_type(self):
        session = requests.session()
        web_url = self.base_url
        response = session.get(url=web_url, headers=self.headers)
        header_item = {'type_name': '', 'icon_name': '', 'parent_id': '', 'parent_name': '', 'type_alias': '',
                       'href': '', "sort": 0}
        if response.status_code == 200:
            print("获得数据成功！")
            html = BeautifulSoup(response.content, 'lxml')
            nav_list = html.select('ul[class="sys_nav"] > li')
            for i in range(0, len(nav_list)):
                nav = nav_list[i]
                a_title = nav.select("li > a")[0]
                icon = a_title.select("i")[0].attrs['class'][1].replace("icon-", "")
                type_name = a_title.get_text()
                if len(type_name) == 0:
                    type_name = '其他'
                header_item['type_name'] = type_name
                header_item['href'] = a_title.attrs['href']
                header_item['icon_name'] = icon
                header_item['sort'] = i + 1
                self._save_item(header_item)
                ul_item_list = nav.select("ul")
                if len(ul_item_list) > 0:
                    ul_item = ul_item_list[0]
                    small_item_list = ul_item.select("li")[0].select("a")
                    for j in range(0, len(small_item_list)):
                        small_header_item = {'type_name': '', 'icon_name': '', 'parent_id': '', 'parent_name': '',
                                             'type_alias': '',
                                             'href': '', "sort": 0}
                        icon_list = small_item_list[j].select("i")
                        if len(icon_list) > 0:
                            temp_icon = icon_list[0].attrs['class'][1].replace("icon-", "")
                            small_header_item['icon_name'] = temp_icon
                        small_header_item['type_name'] = small_item_list[j].get_text()
                        small_header_item['href'] = small_item_list[j].attrs['href']
                        small_header_item['parent_name'] = type_name
                        small_header_item['sort'] = j + 1
                        print(small_header_item)
        else:
            print(str(response.status_code) + "获取数据失败")

    def _save_item(self, item):
        # 先查询，如果存在则更新
        query_one_sql = "select * from bootstrap_type where type_name=%s"
        old_data = self.mysql_pool.select_one(query_one_sql, item['type_name'])
        if old_data is None:
            id = 'Type' + str(self.worker.get_id())
            insert_sql = "insert into bootstrap_type(type_id,type_name,parent_id,parent_name,type_alias,icon_name,href,sort) values (%s,%s,%s,%s,%s,%s,%s,%s)"
            self.mysql_pool.insert_one(insert_sql,
                                       (id, item['type_name'], item['parent_id'], item['parent_name'],
                                        item['type_alias'], item['icon_name'],
                                        item['href'], str(item['sort'])))
            print('新增成功')
        else:
            update_sql = "update bootstrap_type set type_name=%s,parent_id=%s,parent_name=%s,type_alias=%s,icon_name=%s,href =%s,sort=%s where type_id=%s"
            self.mysql_pool.update_one(update_sql,
                                       (item['type_name'], item['parent_id'], item['parent_name'],
                                        item['type_alias'],
                                        item['icon_name'], item['href'], str(item['sort']), old_data['type_id']))
            print('修改成功')


if __name__ == '__main__':
    print("---------------start")
    print(sys.argv)
    print("---------------end sys.argv")
    env = 'dev'
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            env = 'test'
    weather = GetWeather(env)
    weather._get_header_type()
