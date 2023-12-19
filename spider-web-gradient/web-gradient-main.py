import requests
import json
from bs4 import BeautifulSoup
from save_to_mysql import save_items
import time
import platform
import requests


def save_colors_local(json_result):
    # 将json数据保存在当前目录文件news.json 便于查看返回的数据类型
    with open("colors.json", "w", encoding="utf-8") as f:
        # json.dumps 能够把python类型转成json字符串
        # unicode字符串转成中文
        # indent  缩进
        f.write(json.dumps(json_result, ensure_ascii=False, indent=4))


def save_url_image(image_url, title):
    # 下载图片
    url = image_url
    r = requests.get(url)
    # 写入图片
    with open('./images/' + title + '.png', "wb") as f:
        f.write(r.content)


def spider_web_gradient():
    session = requests.session()
    web_url = "https://webgradients.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37"}
    response = session.get(url=web_url, headers=headers)
    print(response.status_code)
    print("获得数据成功！")
    # pretty print
    html = BeautifulSoup(response.content, 'lxml')
    # print(html.prettify())
    # 创建CSS选择器
    result = html.select('div[class="container index_page__content_container"]')
    # print(result)
    items = []
    for page_item in result:
        # print(mg_item)
        gradient_item = page_item.select('div[class="gradient js-gradient"]')
        gradient_item2 = page_item.select('div[class="gradient js-gradient js-appearing-card"]')
        gradient_item3 = gradient_item + gradient_item2
        # print(gradient_item3)
        for one in gradient_item3:
            item = {}
            title = one.select('span[class="gradient__title"]')[0].get_text()
            title = title.replace('\r\n                    ', ' ')
            image_url = one.select('a[class="gradient__download_button js-reach-goal"]')[0].attrs['href']
            css_code = one.select('div[class="gradient__background js-gradient js-see-view-full"]')[0].attrs[
                'data-css-code']
            color_names = one.select('span[class="gradient__color"]')
            print(title)
            print(image_url)
            print(css_code)
            item['title'] = title
            item['image_url'] = image_url
            item['css_code'] = css_code
            item['colors'] = []
            for color in color_names:
                one_color = color.get_text()
                print(one_color)
                item['colors'].append(one_color)
            colors_string = ','.join(str(x) for x in item['colors'])
            item['colors_string'] = colors_string
            print(item)
            items.append(item)

    # 保存一份在本地文件
    save_colors_local(items)
    save_items(items)
    time.sleep(10)


if __name__ == '__main__':
    print("spider of web gradient starts ")
    spider_web_gradient()
