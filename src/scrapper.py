import requests
import lxml
import time
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
chrome_driver_path = "C:/Users/Lenovo LEGION/Desktop/chromedriver.exe"
from selenium.webdriver.common.by import By

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
}


class Scrapper:

    def __init__(self, currency_name):
        self.currency_name = currency_name

    def scrap_articles(self):
        driver = Chrome(executable_path=chrome_driver_path)
        driver.get(f"https://coinmarketcap.com/currencies/{self.currency_name}/news")
        soup = BeautifulSoup(driver.page_source, "lxml")
        paragraphs = soup.find_all(class_="sc-1eb5slv-0 svowul-3 ddtKCV")
        paragraphs_list = []
        for item in paragraphs:
            paragraphs_list.append(item.getText())
        return paragraphs_list
