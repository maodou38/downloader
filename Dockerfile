FROM python:3.8-alpine
MAINTAINER roiding<dingran@ran-ding.ga>
#修改使用阿里云镜像库
RUN echo -e "https://mirrors.aliyun.com/alpine/latest-stable/community/\nhttps://mirrors.aliyun.com/alpine/latest-stable/main/" >/etc/apk/repositories

COPY ./web /downloader
WORKDIR /downloader

#安装所需依赖
# RUN apk update && apk upgrade && apk add --update --no-cache g++ gcc libxslt-dev python3-dev openssl-dev && apk add --no-cache gcc musl-dev libxslt-dev && pip install -r requirement.txt -i https://mirrors.aliyun.com/pypi/simple
RUN apk update && apk upgrade &&pip install gunicorn -i https://mirrors.aliyun.com/pypi/simple && pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
EXPOSE 8080

ENTRYPOINT gunicorn -w 4 -b 0.0.0.0:8080 app:app