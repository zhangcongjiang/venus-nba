import psycopg2
import traceback

import requests
from bs4 import BeautifulSoup
import time

import json
import redis

REDIS_DATA_TIMEOUT = 3 * 24 * 60 * 60


class RedisInfo:
    # redis的相关配置 读取ini文件
    HOST_IP = "10.67.37.131"
    HOST_PORT = 30379
    PASSWORD = "nsf0cus."


# 连接池连接使用，节省了每次连接用的时间
class ControlRedis:
    conn_pool = redis.ConnectionPool(host=RedisInfo.HOST_IP, port=RedisInfo.HOST_PORT, password=RedisInfo.PASSWORD)

    def __init__(self):
        self.client = redis.Redis(connection_pool=self.conn_pool)

    @property
    def conn(self):
        return self.client

    def set_key(self, key, info):
        self.client.set(key, json.dumps(info))

    def get_key(self, key):
        value = self.client.get(key)
        return json.loads(value) if value else None

    def set_key_time(self, key, exp=10 * 60):
        self.client.expire(key, exp)

    def delete_key(self, key):
        if isinstance(key, str):
            self.client.delete(key)
        elif isinstance(key, tuple):
            self.client.delete(*key)

    def query_list(self, list_name, start=0, end=-1):
        all_list = self.client.lrange(name=list_name, start=start, end=end)
        return all_list

    def query_len(self, list_name):
        list_len = self.client.llen(name=list_name)
        return list_len

    def get_left_list(self, list_name):
        value = self.client.lpop(list_name)
        return json.loads(value) if value else None

    def add_right_list(self, list_name, info):
        self.client.rpush(list_name, json.dumps(info))

    def add_left_list(self, list_name, info):
        self.client.lpush(list_name, json.dumps(info))

    def set_lock(self, key, info, exp_time=10 * 60):
        if self.client.setnx(key, info):
            self.client.expire(key, exp_time)
            return True
        return False

    def exists_key(self, key):
        return self.client.exists(key)

    def set_hash_key(self, key, field, value):
        return self.client.hset(key, field, json.dumps(value))

    def get_hash_key(self, key, field):
        value = self.client.hget(key, field)
        return json.loads(value) if value else None

    def get_hash_all(self, key):
        all_value = self.client.hgetall(key)
        temp = {}
        if all_value:
            for k, v in all_value.items():
                k = k.decode()
                v = json.loads(v.decode())
                temp[k] = v
            return temp
        return None

    def del_hash_key(self, key, field):
        return self.client.hdel(key, field)

    def zaddlist(self, key, dict):
        pipe = self.client.pipeline()
        for member, score in dict.items():
            pipe.zadd(key, {member: score})
        pipe.execute()

    def zadd(self, key, score, member):
        return self.client.zadd(key, {score: member})

    def zscan(self, key):
        return self.client.zscan(key)

    def zrangebyscore(self, key, min, max):
        return self.client.zrangebyscore(key, min, max)

    def zremrangebyscore(self, key, start, end):
        return self.client.zremrangebyscore(key, start, end)


class PsqlConnect:

    @staticmethod
    def connect(host, database, user, password, port):
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        return conn


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
    con_list = con.find_all('div', class_="cc-cd")
    data = []
    redis_client = ControlRedis()
    for i in con_list:
        try:
            author = i.find('div', class_='cc-cd-lb').get_text().replace(" ", "").replace("\n", "")  # 获取平台名字
            type = i.find('div', class_='cc-cd-sb-ss').get_text().replace(" ", "").replace("\n", "")

            redis_key = f"{tag}_{author}_{type}_131"
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
        store_data_to_db(data, tag)


def store_data_to_db(data, tag):
    # 连接到数据库
    psql = PsqlConnect()
    conn = psql.connect(host="localhost",
                        database="spider",
                        user="postgres",
                        password="postgres",
                        port="5432")

    print(data)
    sql = f"""INSERT INTO public.hot_{tag} ("author", "type","rank","msg","hots", "category")
            VALUES (%s, %s,%s, %s,%s,%s)
            ON CONFLICT DO NOTHING;
            """

    # data1 = pd.DataFrame(data)
    #
    # f = StringIO()
    # data1.replace('\r', ' ', regex=True).to_csv(f, sep='\t', index=False, header=False)
    # f.seek(0)

    # 创建一个游标对象
    cur = conn.cursor()
    start = int(time.time())
    cur.executemany(sql, data)
    # cur.copy_from(f, f'hot_{tag}', columns=('author', 'type', 'rank', 'msg', 'hots', 'href', 'time', 'category'))
    stop = int(time.time())
    # print(f"写入{tag}数据库耗时：{stop - start}")
    # 提交更改
    conn.commit()
    # 关闭游标和连接
    cur.close()
    conn.close()


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
