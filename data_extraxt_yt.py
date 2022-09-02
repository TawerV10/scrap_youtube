from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as BS
import pandas as pd
import requests
import csv
import time
import random

keyword = input('Keyword: ')

try:
    options = webdriver.ChromeOptions()

    options.add_argument(f'user-agent={UserAgent().random}')
    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.binary_location = 'C:\Program Files\Google\Chrome Beta\Application\chrome.exe'  # Chrome location

    path = r'C:\Users\name\Documents\GitHub\chromedriver.exe'  # driver location
    service = Service(path)
    driver = webdriver.Chrome(service=service, options=options)

    data = []
    with open(f'{keyword}.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'name', 'link', 'subscribers', 'videos'
        ])

    url = f'https://www.youtube.com/results?search_query={keyword}&sp=EgIQAg%253D%253D'
    driver.get(url)

    time.sleep(60)

    channel_lst = driver.find_elements(By.XPATH, "//div[@id='content-section']/div[@id='info-section']/a")
    print(len(channel_lst))

    count = 1
    for channel in channel_lst:
        name = channel.find_element(By.XPATH, "div[@id='info']/ytd-channel-name[@id='channel-title']").text
        link = 'https://www.youtube.com/' + channel.get_attribute('href')
        subscribers = channel.find_element(By.XPATH, "div[@id='info']/div[@id='metadata']/span[@id='subscribers']").text
        videos = channel.find_element(By.XPATH, "div[@id='info']/div[@id='metadata']/span[@id='video-count']").text

        with open(f'{keyword}.csv', 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                name, link, subscribers, videos
            ])

        print(f'{count}.{name} - {link} - {subscribers} - {videos}')
        count += 1

except Exception as ex:
    print(ex)
finally:
    driver.stop_client()
    driver.close()
    driver.quit()