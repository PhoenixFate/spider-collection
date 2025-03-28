import re

html_link = '<a href="https://example.com">Example</a>'

# 使用正则表达式提取URL
url_pattern = r'href="([^"]+)"'  # 匹配以href="开头，紧接着是一个或多个非"字符，然后是"结尾的模式
url_match = re.search(url_pattern, html_link)

if url_match:
    url = url_match.group(1)
    print("提取到的URL：", url)
else:
    print("未找到URL")


html_links = '''
<a href="https://example.com">Example 1</a>
<a href="https://example2.com">Example 2</a>
<a href="https://example3.com">Example 3</a>
'''

# 使用正则表达式提取多个URL
urls = re.findall(r'href="([^"]+)"', html_links)

if urls:
    print("提取到的URL列表：", urls)
else:
    print("未找到URL")


html_links2 = '''
<a url(https://example.com)>Example 1</a>
<a url('https://example.com')>Example 1</a>
<a url("https://example.com")>Example 1</a>
'''
urls2 = re.findall(r'url\(\'?"?([^\'|^"]*)\'?"?\)', html_links2)

if urls2:
    print("提取到的URL列表：", urls2)
else:
    print("未找到URL")
