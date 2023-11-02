import os
import time
import traceback
import uuid
import re

import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from transformers import MarianMTModel, MarianTokenizer
from selenium.webdriver.common.keys import Keys
from tools.redis_tools import ControlRedis
from settings import REDIS_DATA_TIMEOUT
from datetime import datetime, timedelta
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def translate(content):
    # 指定本地文件路径
    model_path = "F:\\pycharm_workspace\\venus\\google\\models\\Helsinki-NLP\\opus-mt-en-zh"

    # 加载模型和标记器
    model = MarianMTModel.from_pretrained(model_path)
    tokenizer = MarianTokenizer.from_pretrained(model_path)
    inputs = tokenizer.encode(content, return_tensors="pt")
    translation_ids = model.generate(inputs)
    translation = tokenizer.decode(translation_ids[0], skip_special_tokens=True)
    return translation


def request_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',  # 声明支持的内容编码方式
        'Connection': 'keep-alive',  # 保持长连接
        'Upgrade-Insecure-Requests': '1',  # 发送HTTPS请求时尝试升级到安全连接
        'Cache-Control': 'max-age=0',  # 控制缓存
        'DNT': '1',  # 表示用户不愿被跟踪
        'Referer': 'https://www.google.com/',  # 引用来源
        'Sec-Fetch-Site': 'same-origin',  # 安全提取网站信息
        'Sec-Fetch-Mode': 'navigate',  # 安全提取模式
        'Sec-Fetch-User': '?1',  # 安全提取用户信息
        'Sec-Fetch-Dest': 'document',  # 安全提取目标
        'TE': 'trailers',  # 指定支持的传输编码
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        search_results = response.text
    else:
        return
    soup = BeautifulSoup(search_results, 'html.parser')

    pattern = re.compile(r'^_article|^_articles')
    detail_pattern = re.compile(r'^_details')

    articles = soup.find_all('div', {'class': pattern})
    articles.extend(soup.find_all('ul', {'class': pattern}))
    article_urls = {}
    redis_client = ControlRedis()
    for article in articles:
        article_url_position = article.find_next('a')
        article_url = article_url_position.get('href', '')
        if 'https' not in article_url:
            continue
        title = article_url_position.find_next('h5').get_text()
        article_urls[article_url] = title

    li_articles = soup.find_all('li', {'class': pattern})
    for li_article in li_articles:
        article_detail = li_article.find_next('div', {'class': detail_pattern})
        if not article_detail:
            continue
        article_url_position = article_detail.find_next('a')
        article_url = article_url_position.get('href', '')
        if 'https' not in article_url:
            continue
        title = article_url_position.find_next('h5').get_text()
        article_urls[article_url] = title

    redis_key = f"nba_daily_news"
    now = int(time.time())
    redis_client.zremrangebyscore(redis_key, -1, now - REDIS_DATA_TIMEOUT)
    exist_redis_data = redis_client.zrangebyscore(redis_key, -1, now)
    redis_add_data = {}

    current_datetime = datetime.now()
    date_string = current_datetime.strftime("%Y-%m-%d")
    file_path = f"F:\\notebooks\\其他\\hoopswire\\{date_string}"
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    for k, v in article_urls.items():
        if v not in exist_redis_data:
            redis_add_data[v] = now
        file_name = os.path.join(file_path, f"{translate(v).replace(' ', '_').replace('?', '？')}.md")
        print(file_name)
        try:
            with open(file_name, "w", encoding="utf-8") as file:
                file.write("<center>" + translate(v) + "</center>\n\n")
                file.write(k + "\n\n")
        except Exception:
            print(traceback)


if __name__ == '__main__':
    while True:
        try:
            start = int(time.time())
            url = "https://sportspyder.com/sports/nba"
            request_url(url)
            end = int(time.time())
            spend = end - start
            time.sleep(1080)
        except Exception:
            print(traceback.format_exc())
            time.sleep(1000)
