import datetime
import time

import psycopg2


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


def get_sql(sql):
    psql = PsqlConnect()
    conn = psql.connect(host="10.67.0.165",
                        database="spider",
                        user="postgres",
                        password="postgres",
                        port="5432")

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
    psql = PsqlConnect()
    conn = psql.connect(host="10.67.0.165",
                        database="spider",
                        user="postgres",
                        password="postgres",
                        port="5432")

    # 创建一个游标对象
    cur = conn.cursor()
    start = int(time.time())
    cur.executemany(sql, data)
    stop = int(time.time())
    print(f"写入数据库耗时：{stop - start},当前时间{datetime.datetime.now()}")
    # 提交更改
    conn.commit()
    # 关闭游标和连接
    cur.close()
    conn.close()


def update_signal(sql, data):
    psql = PsqlConnect()
    conn = psql.connect(host="10.67.0.165",
                        database="spider",
                        user="postgres",
                        password="postgres",
                        port="5432")

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


def insert_game_logs(data):
    sql = """INSERT INTO public.player_regular_gamelog
(player_name, season, game_date, up, playing_time, pts, reb, oreb, dreb, ast, fga, fg, fg3a, fg3, fta, ft, stl, blk, tov, plus_minus, team, opp, game_win)
VALUES('', 0, '', false, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '', false);
"""
