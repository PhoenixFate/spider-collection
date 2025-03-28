import os
import sys
import threading
import time

import requests
import schedule
from bs4 import BeautifulSoup

from save_data import DataSource

encodings_to_try = ["utf-8", 'GBK', 'ISO-8859-1', 'UTF-16']


def save_url_image(image_url, folder):
    image_name = image_url.split("/")[-1]
    # 下载图片
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37",
    }
    r = requests.get(url=image_url, headers=headers)
    if not os.path.exists('./images'):
        os.mkdir('./images/')
    if not os.path.exists('./images/' + folder):
        os.mkdir('./images/' + folder)
    # 写入图片
    with open('./images/' + folder + '/' + image_name, "wb") as f:
        f.write(r.content)


def save_text(file_name, text):
    full_file_name = './html/' + file_name
    print(full_file_name)
    last_slash_index = full_file_name.rfind("/")
    path = full_file_name[:last_slash_index]
    print(path)
    if not os.path.exists(path):
        os.makedirs(path)
        print("make dirs")
    with open(full_file_name, "wb") as f:
        f.write(text)


def save_logo(file_name, logo_content):
    full_file_name = './html/' + file_name
    print(full_file_name)
    last_slash_index = full_file_name.rfind("/")
    path = full_file_name[:last_slash_index]
    print(path)
    if not os.path.exists(path):
        os.makedirs(path)
        print("make dirs")
    with open(full_file_name, "wb") as f:
        f.write(logo_content)


def spider_data():
    print("---------------start")
    print(sys.argv)
    print("---------------end sys.argv")
    env = 'dev'
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            env = 'test'
    data_source = DataSource(env)
    session = requests.session()
    # css列表
    feng_data_url = "https://www.bootstrapmb.com/chajian/css3"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37"}
    response = session.get(url=feng_data_url, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        html = BeautifulSoup(response.content, 'lxml')
        # print(html.prettify())
        print("获得数据成功！")
        end_page = -1
        page_list = html.select('div[class="pagemain"]')
        if len(page_list) > 0:
            page_end_list = page_list[0].select('a[class="end"]')
            if len(page_end_list) > 0:
                end_page_str = page_end_list[0].get_text().replace("... ", "")
                if end_page_str.isdigit():
                    end_page = int(end_page_str)
        item_data = []
        if end_page > 1:
            end_page = end_page + 2
            for page_num in range(1, end_page, 1):
                print("start page: " + str(page_num))
                one_item = {'item_id': '', 'tag': '', 'cover_url': '', 'cover_origin_url': '', 'title': '',
                            'category': '', "size": '', "introduction": '', "has_source": "NO"}
                feng_data_url_page = "https://www.bootstrapmb.com/chajian/css3?page=" + str(page_num)
                response_page = session.get(url=feng_data_url_page, headers=headers)
                if response_page.status_code == 200:
                    one_page = BeautifulSoup(response_page.content, 'lxml')
                    item_list = one_page.select('div[class="item-box"]')
                    if len(item_list) > 0:
                        for item in item_list:
                            item_image = item.select_one('div[class="item-box_imageContainer"]')
                            if item_image is not None:
                                item_image_a = item_image.select_one('a')
                                if item_image_a is not None:
                                    item_id = item_image_a.attrs['href'].replace("/item/", "")
                                    item_image_url = item_image_a.select_one("img").attrs['src']
                                    save_url_image(item_image_url, item_id)
                                    one_item["item_id"] = item_id
                                    image_name = item_image_url.split("/")[-1]
                                    one_item["cover_url"] = image_name
                                    one_item["cover_origin_url"] = item_image_url
                            tag_module = item.select_one('div[class="tagList-module"]')
                            if tag_module is not None:
                                tag_a_list = tag_module.select("a")
                                if len(tag_a_list) > 0:
                                    tag_str = ""
                                    for tag_a in tag_a_list:
                                        tag_str = tag_str + tag_a.get_text() + ','
                                    one_item["tag"] = tag_str[:-1]
                            content_module = item.select_one('div[class="item-box_content"]')
                            if content_module is not None:
                                title = content_module.select_one("a[class='item-box_title']").get_text()
                                one_item["title"] = title.replace(":", "")
                                category = content_module.select_one("div[class='item-box_category']").select_one(
                                    "a").get_text()
                                one_item["category"] = category
                                one_item["big_category"] = "插件"
                                introduction = content_module.select_one("div[class='intro']").get_text().strip()
                                one_item["introduction"] = introduction
                            footer_module = item.select_one('div[class="item-box_footer"]')
                            if footer_module is not None:
                                detail_list = footer_module.select("div[class='item-box_detailsItem']")
                                if len(detail_list) > 0:
                                    for detail in detail_list:
                                        detail_content = detail.get_text()
                                        if "文件大小： " in detail_content:
                                            size = detail_content.replace("文件大小： ", "")
                                            one_item["size"] = size
                            item_data.append(one_item)
                            # data_source.save_item(one_item)
                            spider_data_preview(one_item["item_id"], one_item["title"])


def spider_data_preview(item_id, title):
    session = requests.session()
    # css列表
    preview_url = "https://www.bootstrapmb.com/item/" + item_id + "/preview"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37"}
    response = session.get(url=preview_url, headers=headers)
    if response.status_code == 200:
        html = BeautifulSoup(response.content, 'lxml')
        # print(html.prettify())
        frame_content = html.select_one("iframe[id='iframe1']")
        if frame_content is not None:
            frame_src = frame_content.attrs['src']
            if frame_src is not None:
                spider_frame_content(item_id, frame_src, title)


def spider_frame_content(item_id, preview_src, title):
    session = requests.session()
    headers = {
        "Referer": "https://www.bootstrapmb.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37"}
    response = session.get(url=preview_src, headers=headers)
    if response.status_code == 200:
        html = BeautifulSoup(response.content, 'lxml')
        save_text(title + "/index.html", response.content)
        link_list = html.select('link')
        if len(link_list) > 0:
            for link in link_list:
                href = link.attrs["href"]
                if not href.startswith("http"):
                    if href.startswith("./"):
                        href = href.replace("./", "", 1)
                    if href.endswith(".js") or href.endswith(".css"):
                        link_url = preview_src + "/" + href
                        print(link_url)
                        link_response = session.get(url=link_url, headers=headers)
                        if link_response.status_code == 200:
                            save_text(title + '/' + href, link_response.content)
                    if href.endswith(".png") or href.endswith(".jpg") or href.endswith(".jpeg"):
                        link_url = preview_src + "/" + href
                        print(link_url)
                        link_response = session.get(url=link_url, headers=headers)
                        if link_response.status_code == 200:
                            save_logo(title + '/' + href, link_response.content)
        script_list = html.select('script')
        if len(script_list) > 0:
            for script in script_list:
                print(script)
                if "src" in script.attrs:
                    href = script.attrs["src"]
                    if not href.startswith("http"):
                        if href.startswith("./"):
                            href = href.replace("./", "", 1)
                        if href.endswith(".js") or href.endswith(".css"):
                            link_url = preview_src + "/" + href
                            print(link_url)
                            link_response = session.get(url=link_url, headers=headers)
                            if link_response.status_code == 200:
                                save_text(title + '/' + href, link_response.content)


def job_spider_data():
    threading.Thread(target=spider_data).start()


if __name__ == '__main__':
    print("spider of feng starts successfully")
    # 每一个小时跑一次爬虫
    schedule.every(24).hours.do(job_spider_data)
    schedule.run_all()
    while True:
        schedule.run_pending()
        # 解决一直占用cpu的问题
        time.sleep(1)
