import logging
import time
from abc import abstractmethod

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)


class Crawler():
    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    def crawl(self, question: str):
        pass


def bypass_captcha(url) -> str:
    service = Service(executable_path="driver/chromedriver")
    driver_opts = webdriver.ChromeOptions()
    driver_opts.add_argument("start-maximized")
    # driver_opts.add_argument("--headless")  # for Chrome >= 109
    driver_opts.add_argument("disable-infobars");
    driver_opts.add_argument("--disable-extensions");
    driver_opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver_opts.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(service=service, options=driver_opts)
    try:
        driver.get(url)
        has_results = False
        try:
            driver.find_element(By.XPATH, "//div[@class='search-results']")
            has_results = True
        except NoSuchElementException as e:
            logger.warning(f"not found search-results, looks like it is blocked by captcha")
            WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='search-results']")
            ))
        return driver.page_source
    except Exception as e:
        logger.error(f"failed to open url {url} within selenium {e}")
        return None
    finally:
        driver.quit()


def get_and_wait(url):
    service = Service(executable_path="driver/chromedriver")
    driver_opts = webdriver.ChromeOptions()
    driver_opts.add_argument("start-maximized")
    driver_opts.add_argument("--headless")  # for Chrome >= 109
    driver_opts.add_argument("disable-infobars");
    driver_opts.add_argument("--disable-extensions");
    driver_opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver_opts.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(service=service, options=driver_opts)
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='substories search-results-loaded']")))
        return driver.page_source
    except Exception as e:
        logger.error(f"failed to open url {url} within selenium {e}")
        return None
    finally:
        driver.quit()
