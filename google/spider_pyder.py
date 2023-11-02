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
    chrome_options = Options()

    # 禁用JavaScript
    # chrome_options.add_argument("--disable-javascript")
    # chrome_options.add_argument("--disable-popup-blocking")

    # 初始化Chrome WebDriver并传入选项
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)
    body = driver.find_element("tag name", "body")
    body.send_keys(Keys.END)  # 模拟按下“End”键
    search_results = driver.page_source
    response = requests.get(url)
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
        # try:
        if v not in exist_redis_data:
            redis_add_data[v] = now
        file_name = os.path.join(file_path, f"{translate(v).replace(' ', '_').replace('?', '？')}.md")
        try:
            with open(file_name, "w", encoding="utf-8") as file:
                file.write("<center>" + translate(v) + "</center>\n\n")
                file.write(k + "\n\n")
        except Exception:
            print(traceback)
        #         driver.execute_script(
        #             f"window.open('{k}', '_blank');")
        #         time.sleep(10)
        #         driver.switch_to.window(driver.window_handles[1])
        #         # 最大化
        #         # driver.maximize_window()
        #         # 最小化
        #         driver.minimize_window()
        #         # 等待一些时间以确保搜索结果加载完成
        #         driver.implicitly_wait(30)
        #         # 获取搜索结果
        #         body = driver.find_element("tag name", "body")
        #         body.send_keys(Keys.END)  # 模拟按下“End”键
        #         # 等待一些时间以加载更多数据
        #         time.sleep(2)  # 这里可以根据您的需求进行调整
        #         news_detail_page = driver.page_source
        #
        #         # 检查请求是否成功
        #         soup = BeautifulSoup(news_detail_page, 'html.parser')
        #
        #         news_body = soup.find('article')
        #         if not news_body:
        #             continue
        #         img = news_body.find_next('img')
        #         if img:
        #             img_url = img.get('src')
        #             name = str(uuid.uuid4())
        #             img_name = os.path.join("F:\\notebooks\\其他\\img", f"{name}.png")
        #             response = requests.get(img_url)
        #             if response.status_code == 200:
        #                 with open(img_name, 'wb') as img_file:
        #                     img_file.write(response.content)
        #                     file.write(f"![]({img_name})\n")
        #
        #         news_detail = news_body.get_text()
        #         news_detail = re.sub('\s+', ' ', news_detail).strip()
        #         file.write(news_detail + "\n")
        #         # todo 解析数据并写入文件
        #         driver.close()
        #         time.sleep(1)
        #
        # except Exception:
        #     print(traceback.format_exc())
        # finally:
        #     driver.switch_to.window(driver.window_handles[0])
        #     time.sleep(1)

    # redis_client.zaddlist(redis_key, redis_add_data)

    # time_lines = soup.find_all('span', class_='td-post-date')
    #
    # today = datetime.now()
    #
    # # 计算昨天的日期
    # yesterday = today - timedelta(days=1)
    #
    # # 将日期格式化为所需的形式
    # formatted_date = yesterday.strftime("%B %d, %Y")
    # url_list = []
    # for time_line in time_lines:
    #     text = time_line.get_text()
    #     if formatted_date in text:
    #         previous_h3 = time_line.find_previous('h3')
    #         url_list.append(previous_h3.find_next('a').get('href'))
    #
    # current_datetime = datetime.now()
    # date_string = current_datetime.strftime("%Y-%m-%d")
    # file_name = f"F:\\notebooks\\其他\\hoopswire\\{date_string}.md"
    # with open(file_name, "w", encoding="utf-8") as file:
    #     file.write("<center>" + date_string + " Daily </center>\n\n")
    #     i = 1
    #     for url_detail in url_list:
    #         # 打开谷歌翻译
    #         driver.execute_script(
    #             "window.open('https://translate.google.com/?hl=zh-CN&sl=auto&tl=zh-CN&op=websites', '_blank');")
    #         time.sleep(10)
    #         driver.switch_to.window(driver.window_handles[1])
    #         wait = WebDriverWait(driver, 10)
    #         input_element = wait.until(EC.presence_of_element_located((By.ID, "i48")))
    #         input_element.send_keys(url_detail)
    #         button = driver.find_element(By.XPATH, "//button[@data-idom-class='yHy1rc eT1oJ mN1ivc zhBWDc']")
    #
    #         # 点击按钮
    #         button.click()
    #         time.sleep(10)
    #         driver.switch_to.window(driver.window_handles[2])
    #         # 最大化
    #         # driver.maximize_window()
    #         # 最小化
    #         driver.minimize_window()
    #         # 等待一些时间以确保搜索结果加载完成
    #         driver.implicitly_wait(30)
    #         # 获取搜索结果
    #         body = driver.find_element("tag name", "body")
    #         body.send_keys(Keys.END)  # 模拟按下“End”键
    #         # 等待一些时间以加载更多数据
    #         time.sleep(2)  # 这里可以根据您的需求进行调整
    #         news_detail = driver.page_source
    #
    #         # 检查请求是否成功
    #         soup = BeautifulSoup(news_detail, 'html.parser')
    #         title = soup.find('h1').get_text()
    #         news_body = soup.find('div', class_='td-post-content')
    #         print(title)
    #         # news_text = news_body.get_text()
    #         file.write(f"{str(i)}. {title}\n")  # 写入标题，注意要加上Markdown标题的格式
    #
    #         i += 1
    #         text_body = list(news_body.children)
    #         for news_text in text_body:
    #             if news_text.name != 'p':
    #                 continue
    #             news_detail = news_text.get_text()
    #             file.write(news_detail + "\n")  # 写入内容
    #             img = news_text.find('img')
    #             if img:
    #                 img_url = img.get('src')
    #                 name = str(uuid.uuid4())
    #                 img_name = os.path.join("F:\\notebooks\\其他\\img", f"{name}.png")
    #                 response = requests.get(img_url)
    #                 if response.status_code == 200:
    #                     with open(img_name, 'wb') as img_file:
    #                         img_file.write(response.content)
    #                         file.write(f"![]({img_name})\n")
    #         file.write("\n\n\n")
    #         driver.close()
    #         time.sleep(1)
    #         driver.switch_to.window(driver.window_handles[1])
    #         driver.close()
    #         time.sleep(1)
    #         driver.switch_to.window(driver.window_handles[0])


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
