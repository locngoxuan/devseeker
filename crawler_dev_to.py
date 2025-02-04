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

from crawler import Crawler, get_and_wait

logger = logging.getLogger(__name__)


class DevToCrawler(Crawler, ABC):
    def __init__(self):
        super().__init__("https://dev.to")

    def crawl(self, question):
        logger.info(f"run crawler for dev.to")
        try:
            question = question.strip().replace(" ", "+")
            url = f"{self.url}/search?utf8=%E2%9C%93&q={question}"
            content = get_and_wait(url)
            if content is None:
                return None
            soup = BeautifulSoup(content, 'html.parser')
            result = soup.find('div', class_='substories search-results-loaded')
            if result is None:
                logger.warning(f"not found answer or is blocked by captcha")
                return None
            rows = result.findAll('article', 'crayons-story')
            results = []
            for idx, row in enumerate(rows):
                icon_src = "https://media2.dev.to/dynamic/image/quality=100/https://dev-to-uploads.s3.amazonaws.com/uploads/logos/resized_logo_UQww2soKuUsjaOGNB38o.png"

                summary = row.find('div', class_='summary')
                result_link = row.find('div', class_='crayons-story__indention')
                title = result_link.find('a').text
                href = f"https://dev.to/{result_link.find('a')['href']}"
                short_desc = ""
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
