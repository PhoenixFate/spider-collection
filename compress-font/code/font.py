# 我们可以利用Python中的fonttools库来快捷实现此项需求，它由谷歌开源，自带了若干实用的字体处理相关命令行工具，使用pip install fonttools安装完成后，我们只需要按照下列格式执行命令行工具pyftsubset即可
# pyftsubset 原始字体文件路径 --text=需要保留的字符 --output-file=输出子集字体文件路径
import os
import re

if __name__ == '__main__':
    # 读入目标文本内容
    with open('Chinese3500.txt', encoding='utf-8') as t:
        source_content = t.read()

    with open('fan5000.txt', encoding='utf-8') as t:
        source_content += t.read()

    print(
        'pyftsubset "E:\shenming\python\spider-collection\compress-font\code\ggg.ttf" --text="{}" --output-file="E:\shenming\python\spider-collection\compress-font\code\ggg-mini.ttf"'.format(
            # 去除空白字符后去重
            ''.join(set(re.sub('\s', '', source_content)))
        ))
    # 模拟执行pyftsubset命令生成字体子集
    os.system(
        'pyftsubset "E:\shenming\python\spider-collection\compress-font\code\ggg.ttf" --text="{}" --output-file="E:\shenming\python\spider-collection\compress-font\code\ggg-mini.ttf"'.format(
            # 去除空白字符后去重
            ''.join(set(re.sub('\s', '', source_content)))
        )
    )
