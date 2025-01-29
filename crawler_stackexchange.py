import logging
from abc import ABC
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

from crawler import Crawler

logger = logging.getLogger(__name__)


class StackExchangeCrawler(Crawler, ABC):
    def __init__(self):
        super().__init__("https://stackexchange.com")

    def crawl(self, question):
        logger.info(f"run crawler for stack exchange")
        question = question.strip().replace(" ", "+")
        url = f"{self.url}/search?q={question}"
        response = requests.get(url)
        if response.status_code != 200:
            logger.error(f"failed to get data from stack exchange {response.status_code} {response.text}")
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
        result = soup.find('div', class_='search-results')
        if result is None:
            logger.warning(f"not found answer or is blocked by captcha")
            return None
        rows = result.findAll('div', 'question search-result')
        results = []
        for idx, row in enumerate(rows):
            icon_div = row.find('div', class_='hot-question-site-icon')
            icon_src = icon_div.find('img')['src']

            summary = row.find('div', class_='summary')
            result_link = row.find('div', class_='result-link')
            title = result_link.find('a').text
            href = result_link.find('a')['href']
            short_desc = row.find('div', class_='excerpt').text.strip()
            short_desc = short_desc.rstrip().replace("\n", "")
            results.append({
                "icon": icon_src,
                "title": title,
                "shot_desc": short_desc,
                "link": href
            })
        return results
