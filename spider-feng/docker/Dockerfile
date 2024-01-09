FROM python:3.7.0
MAINTAINER sm516116978@outlook.com
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN mkdir -p /code
COPY ../code /code/
WORKDIR /code
RUN pip3 config set global.index-url http://mirrors.aliyun.com/pypi/simple
RUN pip3 config set install.trusted-host mirrors.aliyun.com
RUN pip3 install pip -U
RUN pip3 install --no-cache-dir -r requirements.txt
ENTRYPOINT python3 /code/spider_feng_main.py