import re
from re import Pattern

import requests


class EasyListRegex:
    def __init__(self):
        self.url = "https://easylist.to/easylist/easylist.txt"
        self.easy_list_raw = requests.get(self.url).content.decode("utf-8")
        self.reg_ex = self._easylist_to_reg_normalize()

    def _easylist_to_reg_normalize(self) -> Pattern[str]:
        """
        Receives a string with easylist rules as input, normalizes it and returns a regular expression.
        @return: normalized easylist as regular expression
        """

        # удаляем комментарии и пустые строки
        self.easy_list_raw = re.sub(
            r'!.*\n',
            '',
            self.easy_list_raw
        )
        self.easy_list_raw = re.sub(
            r'\n+',
            '\n',
            self.easy_list_raw
        )

        # экранируем специальные символы
        self.easy_list_raw = re.sub(
            r'(\W)',
            r'\\\1',
            self.easy_list_raw
        )

        # заменяем доменные имена на регулярные выражения
        self.easy_list_raw = re.sub(
            r'\|([\w\-]+\.)+[\w\-]+(:\d+)?\|',
            '',
            self.easy_list_raw
        )
        self.easy_list_raw = re.sub(
            r'\|([\w\-]+\.)+[\w\-]+\|',
            '',
            self.easy_list_raw
        )
        self.easy_list_raw = re.sub(
            r'\|[\w\-]+\|',
            '',
            self.easy_list_raw
        )

        # заменяем символы шаблонов на регулярные выражения
        self.easy_list_raw = re.sub(
            r'^@@\|\|',
            '',
            self.easy_list_raw,
            flags=re.MULTILINE
        )
        self.easy_list_raw = re.sub(
            r'^\|\|',
            r'^https?\:\/\/[^\/]+',
            self.easy_list_raw,
            flags=re.MULTILINE
        )
        self.easy_list_raw = re.sub(
            r'^\|',
            r'https?\:\/\/[^\/]+\/',
            self.easy_list_raw,
            flags=re.MULTILINE
        )

        regex = re.compile(self.easy_list_raw)
        return regex

    def process(self, url: str) -> str:
        """
        Removes ads from the transferred site.
        @param url: site url
        @return: html string
        """
        html = requests.get(url).content.decode()
        html = self.reg_ex.sub("", html)
        return html
