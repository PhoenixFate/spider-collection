from bs4 import BeautifulSoup
import urllib.request
import json  # 使用了json格式存储

import ssl
from save_to_mysql import save_items

# 全局取消证书验证
ssl._create_default_https_context = ssl._create_unverified_context


def save_json(json_result):
    # 将json数据保存在当前目录文件news.json 便于查看返回的数据类型
    with open("gundam.json", "w", encoding="utf-8") as f:
        # json.dumps 能够把python类型转成json字符串
        # unicode字符串转成中文
        # indent  缩进
        f.write(json.dumps(json_result, ensure_ascii=False, indent=4))


def gundam():
    url = 'https://acg.78dm.net/ct/3178.html'
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    result_html = response.read()
    print(result_html)

    html = BeautifulSoup(result_html, 'lxml')
    print(html.prettify())
    # 创建CSS选择器
    result = html.select('div[class="column is-2-desktop"]')
    print(result)
    items = []
    for mg_item in result:
        # print(mg_item)
        item = {}
        image = "https:" + mg_item.select('img')[0].attrs['data-src']
        print(image)
        mg_name = mg_item.select('p')[0].get_text()
        print(mg_name)
        item['name'] = mg_name
        item['type'] = "MG"
        item['image'] = image
        items.append(item)
    # print(items)
    save_json(items)
    save_items(items)


if __name__ == "__main__":
    gundam()
