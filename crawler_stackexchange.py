import logging
import time
from abc import ABC
from time import time
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from crawler import Crawler, bypass_captcha

logger = logging.getLogger(__name__)


class StackExchangeCrawler(Crawler, ABC):
    def __init__(self):
        super().__init__("https://stackexchange.com")

    def crawl(self, question):
        logger.info(f"run crawler for stack exchange")
        try:
            question = question.strip().replace(" ", "+")
            url = f"{self.url}/search?q={question}"
            content = bypass_captcha(url)
            soup = BeautifulSoup(content, 'html.parser')
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
        except Exception as e:
            logger.error(f"failed to crawl data {e}")
            return None
