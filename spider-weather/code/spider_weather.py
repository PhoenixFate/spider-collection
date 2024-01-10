import copy
import datetime
import json
import sys
from concurrent.futures import ThreadPoolExecutor

import pymysql
import requests
import schedule
from bs4 import BeautifulSoup

from MySQLConnectionPool import MySQLConnectionPool
from snow import IdWorker


def get_connection(host, port, db, user, password):
    conn = pymysql.connect(host=host, port=port, db=db, user=user, password=password)
    return conn


class GetWeather:
    def __init__(self, environment):
        self.environment = environment
        self.base_url = r"http://www.weather.com.cn/weather/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37"}
        self.area_list = []
        self.mysql_pool = MySQLConnectionPool(environment)
        self.worker = IdWorker(1, 2, 0)
        print(self.mysql_pool)
        with open("city.json", 'r', encoding='UTF-8') as load_f:
            load_list = json.load(load_f)  # 34个省份
            for key, value in load_list.items():
                for key2, value2 in value.items():
                    for key3, value3 in value2.items():
                        area = {'province': key, 'city': key2, 'area_name': key3, "area_id": value3['AREAID']}
                        self.area_list.append(area)
        print(len(self.area_list))

    def __getWeatherInfo__(self):
        # 创建一个包含2条线程的线程池
        if self.environment == 'test':
            pool = ThreadPoolExecutor(max_workers=10)
        else:
            pool = ThreadPoolExecutor(max_workers=60)
        for area in self.area_list:
            future = pool.submit(self.__get_one_weather, area)

    def __get_one_weather(self, area):
        session = requests.session()
        web_url = self.base_url + area['area_id'] + ".shtml"
        response = session.get(url=web_url, headers=self.headers)
        one_weather = copy.copy(area)
        one_weather['weather_chinese'] = ''
        one_weather['date'] = ''
        one_weather['datetime'] = ''
        one_weather['day_temperature'] = ''
        one_weather['night_temperature'] = ''
        one_weather['wind_direction'] = ''
        one_weather['wind_power'] = ''
        if response.status_code == 200:
            print("获得数据成功！")
            html = BeautifulSoup(response.content, 'lxml')
            today_day_list = html.select('li[class="sky skyid lv1 on"]')
            other_day_list = html.select('li[class="sky skyid lv1"]')
            today_day_list2 = html.select('li[class="sky skyid lv2 on"]')
            other_day_list2 = html.select('li[class="sky skyid lv2"]')
            seven_day_list = today_day_list + today_day_list2 + other_day_list + other_day_list2
            for i in range(0, len(seven_day_list)):
                temp_today = seven_day_list[0].select("h1")[0].get_text().replace("日（今天）", "")
                minus = 0
                if int(temp_today) != int(datetime.datetime.now().strftime("%d")):
                    minus = 1
                one_day = seven_day_list[i]
                one_weather['date'] = (datetime.datetime.now() + datetime.timedelta(days=i - minus)).strftime(
                    "%Y-%m-%d")
                one_weather['datetime'] = (datetime.datetime.now() + datetime.timedelta(days=i - minus)).strftime(
                    "%Y-%m-%d %H:%M:%S")
                weather_chinese = one_day.select('p[class="wea"]')[0].get_text()
                one_weather['weather_chinese'] = weather_chinese
                temperature = one_day.select('p[class="tem"]')[0]
                if temperature is not None:
                    span_list = temperature.select("span")
                    if len(span_list) > 0:
                        day_temperature = span_list[0].get_text()
                        one_weather['day_temperature'] = day_temperature
                    i_list = temperature.select("i")
                    if len(i_list) > 0:
                        night_temperature = i_list[0].get_text()
                        one_weather['night_temperature'] = night_temperature
                wind = one_day.select('p[class="win"]')[0]
                one_weather['wind_list'] = []
                if wind is not None:
                    em_list = wind.select("em")
                    if len(em_list) > 0:
                        span_list = em_list[0].select("span")
                        if len(span_list) > 0:
                            for one_wind in span_list:
                                wind_chinese = one_wind.attrs['title']
                                one_weather['wind_list'].append(wind_chinese)
                    i_list = wind.select("i")
                    if len(i_list) > 0:
                        wind_power = i_list[0].get_text()
                        one_weather['wind_power'] = wind_power
                if len(one_weather['wind_list']) > 0:
                    colors_string = ','.join(str(x) for x in one_weather['wind_list'])
                    one_weather['wind_direction'] = colors_string
                if one_weather['day_temperature'] is not None and one_weather['day_temperature'] != '':
                    self.save_item(one_weather)
                print(one_weather)
        else:
            print(str(response.status_code) + "获取数据失败")

    def delete_item(self, item):
        delete_sql = "delete from weather where area_id=%s and weather_date=%s"
        self.mysql_pool.delete_one(delete_sql, item['area_id'], item['date'])
        print('删除成功')

    def save_item(self, item):
        # 先查询，如果存在则更新
        query_one_sql = "select * from weather where area_id=%s and weather_date=%s"
        old_data = self.mysql_pool.select_one(query_one_sql, item['area_id'], item['date'])
        if old_data is None:
            snow_id = 'Wea' + str(self.worker.get_id())
            insert_sql = "insert into weather(weather_id,province,city,area_name,area_id,weather_date,weather_datetime,weather_chinese,day_temperature,night_temperature,wind_direction,wind_power) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.mysql_pool.insert_one(insert_sql,
                                       (snow_id, item['province'], item['city'], item['area_name'],
                                        item['area_id'], item['date'],
                                        item['datetime'], item['weather_chinese'], item['day_temperature'],
                                        item['night_temperature'],
                                        item['wind_direction'], item['wind_power']))
            print('新增成功')
        else:
            update_sql = "update weather set weather_datetime=%s,weather_chinese=%s,day_temperature=%s,night_temperature=%s,wind_direction=%s,wind_power =%s where weather_id=%s"
            self.mysql_pool.update_one(update_sql,
                                       (item['datetime'], item['weather_chinese'], item['day_temperature'],
                                        item['night_temperature'],
                                        item['wind_direction'], item['wind_power'], old_data['weather_id']))
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
    if env == 'dev':
        weather.__getWeatherInfo__()
    # 每一个小时跑一次爬虫
    schedule.every().day.at('10:55').do(weather.__getWeatherInfo__)
    while True:
        schedule.run_pending()
