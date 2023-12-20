import json
import time

import requests
from bs4 import BeautifulSoup

from save_to_mysql import save_items


def save_colors_local(json_result):
    # 将json数据保存在当前目录文件news.json 便于查看返回的数据类型
    with open("colors.json", "w", encoding="utf-8") as f:
        # json.dumps 能够把python类型转成json字符串
        # unicode字符串转成中文
        # indent  缩进
        f.write(json.dumps(json_result, ensure_ascii=False, indent=4))


def spider_japanese_color():
    session = requests.session()
    web_url = "https://nipponcolors.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37"}
    response = session.get(url=web_url, headers=headers)
    print(response.status_code)
    print("获得数据成功！")
    # pretty print
    html = BeautifulSoup(response.content, 'lxml')
    # print(html.prettify())
    # 创建CSS选择器
    result = html.select('ul[id="colors"]')
    # print(result)
    items = []
    for page_item in result:
        color_item = page_item.select('a[href="javascript:void(0);"]')
        web_url2 = "https://nipponcolors.com/php/io.php"
        headers2 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37"}
        for one in color_item:
            item = {}
            name = one.get_text()
            names = name.split(", ")
            color_name = names[0]
            color_key = names[-1]
            data = {
                "color": color_key
            }
            item['color_name'] = color_name
            item['color_key'] = color_key

            response2 = session.post(url=web_url2, headers=headers2, data=data)
            print(response2.status_code)
            print("颜色详情 获得数据成功！")
            json_result = json.loads(response2.content.decode("utf-8"))
            print(json_result)
            item['color_index'] = json_result['index']
            item['cmyk'] = json_result['cmyk']
            item['rgb'] = json_result['rgb']
            items.append(item)
    # 保存一份在本地文件
    save_colors_local(items)
    save_items(items)
    time.sleep(10)


if __name__ == '__main__':
    print("spider of japanese color starts ")
    spider_japanese_color()
