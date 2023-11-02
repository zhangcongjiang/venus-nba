import os.path
import time
import traceback
import uuid
import io

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import re
import requests
import random
import hashlib
from PIL import Image

from collector.database import PsqlConnect
from settings import GOOGLE_SEARCH_TIMEOUT
from tools.redis_tools import ControlRedis
from transformers import MarianMTModel, MarianTokenizer


#https://www.rotoballer.com/player-news?sport=nba  nba daily

def translate(content):
    # 指定本地文件路径
    model_path = "F:\\pycharm_workspace\\venus\\google\\models\\Helsinki-NLP\\opus-mt-en-zh"

    # 加载模型和标记器
    model = MarianMTModel.from_pretrained(model_path)
    tokenizer = MarianTokenizer.from_pretrained(model_path)
    inputs = tokenizer.encode(content, return_tensors="pt")
    translation_ids = model.generate(inputs)
    translation = tokenizer.decode(translation_ids[0], skip_special_tokens=True)
    print("翻译结果：", translation)
    return translation


def store_data_to_db(data, search_info):
    # 连接到数据库
    psql = PsqlConnect()
    conn = psql.connect(host="localhost",
                        database="spider",
                        user="postgres",
                        password="postgres",
                        port="5432")

    print(data)
    sql = f"""INSERT INTO public.google_search ("title", "url","keywords","image_name")
            VALUES (%s, %s, %s,%s)
            ON CONFLICT DO NOTHING;
            """

    # 创建一个游标对象
    cur = conn.cursor()
    start = int(time.time())
    cur.executemany(sql, data)
    stop = int(time.time())
    print(f"写入{search_info}数据库耗时：{stop - start},当前时间{datetime.now()}")
    # 提交更改
    conn.commit()
    # 关闭游标和连接
    cur.close()
    conn.close()


def handle_result(search_results, search_info):
    soup = BeautifulSoup(search_results, 'html.parser')
    results = soup.find_all("div", class_="tF2Cxc")

    data = []
    redis_client = ControlRedis()
    # 提取标题和URL并翻译标题
    for result in results:

        redis_key = f"google_search"
        now = int(time.time())

        redis_client.zremrangebyscore(redis_key, -1, now - GOOGLE_SEARCH_TIMEOUT)
        exist_redis_data = redis_client.zrangebyscore(redis_key, -1, now)
        exist_msg = [item.decode('utf-8') for item in exist_redis_data]

        title = result.find("h3").get_text()
        url = result.find("a")["href"]
        redis_add_data = {}
        if url not in exist_msg:
            translation = translate(title)
            image_id = str(uuid.uuid4())
            data.append((translation, url, search_info, image_id))
            redis_add_data[url] = now

        redis_client.zaddlist(redis_key, redis_add_data)

    if data:
        store_data_to_db(data, search_info)
    return data


if __name__ == '__main__':

    while True:
        driver = webdriver.Chrome()
        search_infos = ['nba top', 'houston rockets', 'Los Angeles Lakers', 'nba draft']
        for key in search_infos:

            try:
                google_url = "https://www.google.com/search?q=" + key

                # 计算一小时前的时间
                one_hour_ago = datetime.now() - timedelta(hours=1)

                # 格式化时间为谷歌搜索的时间范围字符串
                time_range = f"&tbs=qdr:h,sbd:1&cdr:1,cd_min:{one_hour_ago.strftime('%m/%d/%Y %H:%M:%S')}"

                # 构建最终的搜索URL
                search_url = google_url + time_range
                print(search_url)
                # 打开Google网站
                driver.get(search_url)
                # 最大化
                # driver.maximize_window()
                # 最小化
                driver.minimize_window()
                # 等待一些时间以确保搜索结果加载完成
                driver.implicitly_wait(10)

                body = driver.find_element("tag name", "body")
                body.send_keys(Keys.END)  # 模拟按下“End”键

                # 等待一些时间以加载更多数据
                time.sleep(2)  # 这里可以根据您的需求进行调整

                # 再次模拟下拉刷新以加载更多数据
                body.send_keys(Keys.END)

                # 继续等待以加载更多数据
                time.sleep(2)

                # 获取搜索结果
                search_results = driver.page_source
                print(f"key words {key} search successful")
                datas = handle_result(search_results, key)

                time.sleep(60)
            except Exception:
                print(traceback.format_exc())

        time.sleep(60 * 30)
