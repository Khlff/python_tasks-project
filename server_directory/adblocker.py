import re
import urllib.request

import requests


class EasyListLiteRegex:
    def __init__(self):
        self.url = "https://easylist.to/easylist/easylist.txt"

        self.content = str(requests.get(self.url).content)

        self.content = re.sub(r'!.*\n', '', self.content)
        self.content = re.sub(r'\n+', '\n', self.content)

        self.content = re.sub(r'(\W)', r'\\\1', self.content)

        self.content = re.sub(r'\|([\w\-]+\.)+[\w\-]+(\:\d+)?\|', '',
                              self.content)
        self.content = re.sub(r'\|([\w\-]+\.)+[\w\-]+\|', '', self.content)
        self.content = re.sub(r'\|[\w\-]+\|', '', self.content)

        self.content = re.sub(r'^@@\|\|', '', self.content, flags=re.MULTILINE)
        self.content = re.sub(r'^\|\|', r'^https?\:\/\/[^\/]+', self.content,
                              flags=re.MULTILINE)
        self.content = re.sub(r'^\|', r'https?\:\/\/[^\/]+\/', self.content,
                              flags=re.MULTILINE)

        self.regex = re.compile(self.content)

    def process(self, url):
        html = requests.get(url).content.decode()
        html = self.regex.sub("", html)
        with open("test.html", "w", encoding="utf-8") as f:
            f.write(html)


lox = EasyListLiteRegex()
lox.process("https://habr.com/ru/articles/724232/")