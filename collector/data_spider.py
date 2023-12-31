import traceback

import requests
from bs4 import BeautifulSoup
import time

import logging
from logging.handlers import TimedRotatingFileHandler
from settings import REDIS_DATA_TIMEOUT
from tools.redis_tools import ControlRedis
from tools.sqlUtils import store_to_db

# 创建一个logger
logger = logging.getLogger('nba.log')
logger.setLevel(logging.DEBUG)

# 创建一个handler，用于写入日志文件，每天切换一次
log_file_path = "/var/log/venus/nba.log"
handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, backupCount=15)
handler.suffix = "%Y%m%d"
handler.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# 将handler添加到logger中
logger.addHandler(handler)


def download_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
    try:
        r = requests.get(url, timeout=30, headers=headers)
        return r.text
    except:
        return "please inspect your url or setup"


def get_content(html, tag):
    soup = BeautifulSoup(html, 'html.parser')
    con = soup.find('div', attrs={'class': 'bc-cc'})
    if not con:
        return
    con_list = con.find_all('div', class_="cc-cd")
    data = []
    redis_client = ControlRedis()
    for i in con_list:
        try:
            author = i.find('div', class_='cc-cd-lb').get_text().replace(" ", "").replace("\n", "")  # 获取平台名字
            type = i.find('div', class_='cc-cd-sb-ss').get_text().replace(" ", "").replace("\n", "")

            redis_key = f"{tag}_{author}_{type}"
            now = int(time.time())
            redis_client.zremrangebyscore(redis_key, -1, now - REDIS_DATA_TIMEOUT)
            exist_redis_data = redis_client.zrangebyscore(redis_key, -1, now)
            exist_msg = [item.decode('utf-8') for item in exist_redis_data]

            link = i.find('div', class_='cc-cd-cb-l').find_all('a')  # 获取所有链接
            redis_add_data = {}
            for k in link:
                # href = k['href']
                rank = k.find('span', class_='s').get_text()

                hot = str(k.find('span', class_='e').get_text())

                # date_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                msg = str(k.find('span', class_='t').get_text()).replace('\r', ' ')

                if msg not in exist_msg:
                    data.append((author, type, int(rank), msg, hot, tag))
                    redis_add_data[msg] = now
                    # print(f"msg: {msg} ,来源：{author}：{type}")

            redis_client.zaddlist(redis_key, redis_add_data)
        except Exception:
            # print(traceback.format_exc())
            pass

    if data:
        sql = f"""INSERT INTO public.hot_{tag} ("author", "type","rank","msg","hots", "category")
                VALUES (%s, %s,%s, %s,%s,%s)
                ON CONFLICT DO NOTHING;
                """
        logger.info(data)
        store_to_db(sql, data)


def main():
    base_url = 'https://tophub.today'
    html = download_page(base_url)
    get_content(html, 'shopping')
    tags = ['news', 'tech', 'ent', 'developer', 'community']
    # tags = ['news']
    for tag in tags:
        html = download_page(f"{base_url}/c/{tag}")
        get_content(html, tag)


if __name__ == '__main__':
    while True:
        try:
            start = int(time.time())
            main()
            end = int(time.time())
            spend = end - start
            if spend < 240:
                time.sleep(300 - spend)
            else:
                time.sleep(60)
        except Exception:
            print(traceback.format_exc())

    # try:
    #     main()
    # except Exception:
    #     print(traceback.format_exc())
