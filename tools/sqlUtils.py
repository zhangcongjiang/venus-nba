import datetime
import time

import psycopg2


class Psql:

    @staticmethod
    def connect():
        #云端
        conn = psycopg2.connect(host="39.98.165.125",
                                database="siper",
                                user="postgres",
                                password="nsf0cus.@123",
                                port="12345")
        #本地
        # conn = psycopg2.connect(host="10.67.0.165",
        #                         database="spider",
        #                         user="postgres",
        #                         password="postgres",
        #                         port="5432")
        return conn


def get_sql(sql):
    psql = Psql()
    conn = psql.connect()

    cur = conn.cursor()

    cur.execute(sql)
    rows = cur.fetchall()

    # 定义一个空列表，用于存储转换后的字典
    result = []

    # 遍历查询结果，并将每一行转换为字典
    for row in rows:
        # 将查询结果的列名和对应的值组成键值对，并添加到字典中
        row_dict = dict(zip([column[0] for column in cur.description], row))
        # 将字典添加到结果列表中
        result.append(row_dict)

    cur.close()
    conn.close()

    return result


def store_to_db(sql, data):
    # 连接到数据库
    psql = Psql()
    conn = psql.connect()

    # 创建一个游标对象
    cur = conn.cursor()
    start = int(time.time())
    cur.executemany(sql, data)
    stop = int(time.time())
    print(f"{len(data)}条数据，写入数据库耗时：{stop - start},当前时间{datetime.datetime.now()}")
    # 提交更改
    conn.commit()
    # 关闭游标和连接
    cur.close()
    conn.close()


def update_signal(sql, data):
    psql = Psql()
    conn = psql.connect()

    # 创建一个游标对象
    cur = conn.cursor()

    # 提供更新操作的参数（这里以两个参数为例）
    update_values = ("new_value", "condition_value")

    # 执行更新操作
    cur.execute(sql, data)

    # 提交更改
    conn.commit()

    # 关闭游标和连接
    cur.close()
    conn.close()
