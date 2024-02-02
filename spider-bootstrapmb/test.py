from pywebcopy import save_webpage, save_website


def clone_website(url, dest_folder):
    save_website(
        url=url,
        project_folder=dest_folder,
        # 可选参数，设置代理服务器等其他参数
    )


# bypass_robots_txt：设置为 True 可以忽略 Robots.txt 文件限制。
# overwrite：设置为 True 可以覆盖已存在的文件。
# depth：设置克隆的深度。
# connection_timeout：设置连接超时时间。
def clone_website_advanced(url, dest_folder):
    # save_website(
    #     url=url,
    #     project_folder=dest_folder,
    #     open_in_browser=False,
    #     bypass_robots=False
    # )
    save_website(
        url=url,
        project_folder=dest_folder,
        project_name="my_site",
        bypass_robots=False,
    )


# 指定要克隆的网页 URL 和目标文件夹
url_to_clone = "https://v.bootstrapmb.com/2023/8/e6mh214015/index.html"
destination_folder = "./folder"

# 调用克隆函数
clone_website_advanced(url_to_clone, destination_folder)
