import urllib3
from urllib import parse
import requests
import re
from faker import Faker
# 由于lxml需要用到系统库 非常大
# from lxml import html

urllib3.disable_warnings()


class Parser:
    def __init__(self, url, web):
        self.url = url
        self.web = web
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': Faker().user_agent()})
        self.session.verify = False

        self.proxies = {}

    def parse(self):
        if self.web == 'mayiyingshi':
            return self.parseMayiyingshi()

    def parseMayiyingshi(self):
        # 开始读取第一次的源地址
        url = self.getScript(self.url, 'player_data')
        index = self.getScript(url, "index.m3u8")
        return parse.urljoin(url, index)

    def getScript(self, url, pattern):
        html1 = self.session.get(url).text
        # scripts = html.etree.HTML(html1).xpath('//script/text()')
        scripts = re.findall("<script[\s\S]*?>[\s\S]*?<\/script>", html1)
        # 获取特定script标签的内容，不包含标签本身
        script = list(filter(lambda x: (pattern in x), scripts))[0]
        pattern = "\"url\":\"(.*?)\""
        match = re.search(pattern, script)
        if not match:
            pattern = "url:\s?'(.*?)',"
            match = re.search(pattern, script)
        return re.sub("\\\\", "", match.group(1))
