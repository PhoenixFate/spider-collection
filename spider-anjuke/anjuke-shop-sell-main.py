import re

import requests
import json
from bs4 import BeautifulSoup
from save_to_mysql import save_shop_sell_item
import time
import platform
import requests
import decimal


def spider_anjuke_shop_sell_main():
    name_key = [
                   {
                       "name": "wujin",
                       "start": 1,
                       "max": 11
                   },
                   {
                       "name": "xinbei",
                       "start": 1,
                       "max": 7
                   },
                   {
                       "name": "tianning",
                       "start": 1,
                       "max": 8
                   },
                   {
                       "name": "zhonglou",
                       "start": 1,
                       "max": 9
                   },
                   {
                       "name": "czjingkaiqu",
                       "start": 1,
                       "max": 2
                   },
               ],
    name_key2 = [
        {
            "name": "zhonglou",
            "start": 3,
            "max": 9
        },
        {
            "name": "czjingkaiqu",
            "start": 1,
            "max": 2
        },
    ]
    for one_name in name_key2:
        start = one_name["start"]
        max_page = one_name["max"]
        name = one_name["name"]
        for num in range(start, max_page):
            session = requests.session()
            web_url = "https://cz.sydc.anjuke.com/sp-shou/" + name + "-p" + str(
                num) + "/?maxInserted=0&skuInserted=0&zzvipInserted=0"
            print(web_url)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
            response = session.get(url=web_url, headers=headers)
            if response is not None and response.status_code == 200:
                print(response.status_code)
                print("获得数据成功！")
                # pretty print
                html = BeautifulSoup(response.content, 'lxml')
                # print(html.prettify())
                # 创建CSS选择器
                result = html.select_one('div[class="list-left"]')
                # print(result)
                house_list = []
                if result is None:
                    print("no result !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    break
                else:
                    item_list = result.select('div[class="list-item"]')
                    if item_list is not None:
                        for item in item_list:
                            house = {'title': '', 'address': '', 'price': '', 'price_short': '', 'price_str': '',
                                     'price_unit': '',
                                     'price_total': '', 'area': '', 'street': '', 'region': ''}

                            house_url = item.select('a')[0].attrs['href']
                            print(house_url)
                            pattern = r'houseid=(\d+)'
                            match_obj = re.search(pattern, house_url)
                            if match_obj:
                                house['house_id'] = match_obj.group(1)
                                print("house_id:" + match_obj.group(1))  # 输出hello world，完整的匹配字符串

                            item_info = item.select_one('div[class="item-info"]')
                            if item_info is not None:
                                title = item_info.select_one('span[class="title"]')
                                if title is not None:
                                    title_content = title.get_text()
                                    house['title'] = title_content
                            descript_list = item.select('p[class="item-descript"]')
                            if descript_list is not None and len(descript_list) > 0:
                                desc = descript_list[0]
                                span_list = desc.select("span")
                                if span_list is not None and len(span_list) > 0:
                                    region = span_list[0].get_text()
                                    house['region'] = region
                                    if len(span_list) > 1:
                                        street = span_list[1].get_text().replace("- ", "")
                                        house['street'] = street
                                    if len(span_list) > 2:
                                        address = span_list[2].get_text().replace("- ", "").replace("|", "")
                                        house['address'] = address
                            item_area = item.select_one('div[class="item-area"]')
                            if item_area is not None:
                                area_p = item_area.select_one('p[class="area"]')
                                if area_p is not None:
                                    span_list = area_p.select('span')
                                    if span_list is not None and len(span_list) > 0:
                                        area = span_list[0].get_text()
                                        house['area'] = area
                            item_price = item.select_one('div[class="item-price"]')
                            if item_price is not None:
                                price_div = item_price.select_one('div[class="price-daily"]')
                                if price_div is not None:
                                    span_list = price_div.select('span')
                                    if span_list is not None and len(span_list) > 0:
                                        if len(span_list) > 1:
                                            price = span_list[1].get_text()
                                            if len(span_list) > 2:
                                                price_unit = span_list[2].get_text()
                                                house['price_unit'] = price_unit
                                                house['price_str'] = price + price_unit
                                                house['price_short'] = price
                                                if price_unit == '万/m²':
                                                    price = decimal.Decimal(price) * 10000
                                            house['price'] = str(price)
                                price_total_div = item_price.select_one('div[class="price-monthly"]')
                                if price_total_div is not None:
                                    span_list = price_total_div.select('span')
                                    if span_list is not None and len(span_list) > 0:
                                        price_total = span_list[0].get_text()
                                        house['price_total'] = price_total
                            session2 = requests.session()
                            response2 = session2.get(url=house_url, headers=headers)
                            html2 = BeautifulSoup(response2.content, 'lxml')
                            script_list = html2.select('script[type="text/javascript"]')
                            # if script_list is not None and len(script_list) > 0:
                            #     script_list[0].get_text()
                            house['lat'] = 0.0
                            house['lng'] = 0.0
                            for script_one in script_list:
                                script_text = script_one.get_text()
                                # print(script_text)
                                pattern = r'lat: (\d+).(\d+),'
                                match_obj = re.search(pattern, script_text)
                                print(match_obj)
                                if match_obj:
                                    house['lat'] = match_obj.group(1) + "." + match_obj.group(2)
                                pattern2 = r'lng: (\d+).(\d+),'
                                match_obj2 = re.search(pattern2, script_text)
                                if match_obj2:
                                    house['lng'] = match_obj2.group(1) + "." + match_obj2.group(2)
                            # time.sleep(3)
                            house_list.append(house)
                            print(house)
                            save_shop_sell_item(house)
                            print("------------------------------")
            time.sleep(10)


if __name__ == '__main__':
    print("spider of anjuku shop sell starts ")
    spider_anjuke_shop_sell_main()
