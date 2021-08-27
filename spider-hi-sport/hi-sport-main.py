import requests
import json
from bs4 import BeautifulSoup
from save_to_mysql import save_items
import time


def save_food_local(json_result):
    # 将json数据保存在当前目录文件news.json 便于查看返回的数据类型
    with open("food.json", "w", encoding="utf-8") as f:
        # json.dumps 能够把python类型转成json字符串
        # unicode字符串转成中文
        # indent  缩进
        f.write(json.dumps(json_result, ensure_ascii=False, indent=4))


def spider_hi_sport():
    session = requests.session()
    food_type = ['谷薯芋、杂豆、主食', '蛋类、肉类及制品', '奶类及制品']
    for page in range(5):
        print("page: " + str(page))
        food_data_url = "https://food.hiyd.com/list-1-html?page=" + str(page)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37"}
        response = session.get(url=food_data_url, headers=headers)
        print(response.status_code)
        print("获得数据成功！")
        # pretty print
        html = BeautifulSoup(response.content, 'lxml')
        # print(html.prettify())
        # 创建CSS选择器
        result = html.select('div[class="box-bd"] ul li')
        # print(result)
        items = []
        for food_item in result:
            # print(mg_item)
            item = {}
            image = food_item.select('div[class="img-wrap"] img')[0].attrs['src']
            name = food_item.select('div[class="cont"] h3')[0].get_text()
            hot = food_item.select('div[class="cont"] p')[0].get_text()[3:]
            item['name'] = name
            item['image'] = image
            item['hot'] = hot
            item['page'] = page
            item["type"] = food_type[0]
            items.append(item)
        # 保存一份在本地文件
        save_food_local(items)
        save_items(items)
        time.sleep(10)


if __name__ == '__main__':
    print("spider of hi-sport starts successfully")
    spider_hi_sport()
