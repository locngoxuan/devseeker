from abc import ABC
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

from crawler import Crawler


class StackExchangeCrawler(Crawler, ABC):
    def __init__(self):
        super().__init__("https://stackexchange.com")

    def crawl(self, question):
        question = question.strip().replace(" ", "+")
        url = f"{self.url}/search?q={quote(question)}"
        response = requests.get(url)
        if response.status_code != 200:
            return None
        content = response.content.decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')
        head_element = soup.find('head')
        if head_element is not None:
            head_element.extract()
        extract_script = True
        while extract_script:
            s = soup.find('script')
            if s is not None:
                s.extract()
            else:
                extract_script = False
        results = soup.find('div', class_='flush-left js-search-results')
        print(results.prettify())
