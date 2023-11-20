import datetime
import random

import requests
from bs4 import BeautifulSoup
import time

from selenium.webdriver.firefox.options import Options
import psycopg2

from tools.sqlUtils import update_signal


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


def execute_sql(sql):
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


def store_data_to_db(sql, data):
    # 连接到数据库
    psql = PsqlConnect()
    conn = psql.connect(host="10.67.0.165",
                        database="spider",
                        user="postgres",
                        password="postgres",
                        port="5432")

    # print(data)

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


def requests_url(url):
    headers = {
        'authority': 'www.basketball-reference.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    return response.text


def handle_selary(all_salaries):
    salaries = {}

    if all_salaries:
        tbody = all_salaries.find('tbody')
        trs = tbody.find_all('tr')
        for tr in trs:
            key = tr.find_next('th').text
            sala = int(tr.find('td', {'data-stat': 'salary'}).get('csk', 0))
            if key not in salaries.keys():
                salaries[key] = sala
            else:
                salaries[key] += sala
            sql = """UPDATE public.player_regular_total_season SET salary=%s WHERE href=%s and season =%s;"""
            data = (salaries[key], player_url, key)
            update_signal(sql, data)
    print(player_id, player_name, salaries)


#
# if __name__ == '__main__':
#     sql = """SELECT id,player_name,href FROM public.player_draft where attend=TRUE and id>200;"""
#     players = execute_sql(sql)
#     sorted_players = sorted(players, key=lambda x: x['id'])
#     for player in sorted_players:
#         print(player)
#         player_name = player.get('player_name')
#         player_url = player.get('href')
#         player_id = player.get('id')
#
#         url = f"https://www.basketball-reference.com{player_url}"
#         # 用requests方法
#         search_result = requests_url(url)
#
#         soup = BeautifulSoup(search_result, 'html.parser')
#
#         if soup.find('table', {'id': 'all_salaries'}):
#             all_salaries = soup.find('table', {'id': 'all_salaries'})
#             handle_selary(all_salaries)
#         else:
#             # 找到所有注释
#             comments = soup.find_all(string=lambda text: isinstance(text, Comment))
#             comment_contents = []  # 保存注释内容的列表
#             for comment in comments:
#                 comment_contents.append(comment)
#
#             for com in comment_contents:
#                 comment_soup = BeautifulSoup(com, 'html.parser')
#                 if comment_soup.find('table', {'id': 'all_salaries'}):
#                     all_salaries = comment_soup.find('table', {'id': 'all_salaries'})
#                     handle_selary(all_salaries)
#         random_number = random.randint(15, 20)
#         time.sleep(random_number)

if __name__ == '__main__':
    sql = """SELECT id,player_name,href FROM public.player_active where  id=390;"""
    players = execute_sql(sql)
    for player in players:
        player_name = player.get('player_name')
        player_url = player.get('href')
        player_id = player.get('id')
        options = Options()

        # options.add_argument('-headless')
        options.set_preference('permissions.default.image', 2)  # 禁止加载图片
        options.set_preference('permissions.default.stylesheet', 2)  # 禁止加载CSS
        options.set_preference('permissions.default.script', 2)  # 禁止加载JavaScript
        options.set_preference('permissions.default.video', 2)  # 禁止加载视频

        url = f"https://www.basketball-reference.com{player_url}"
        # 用requests方法
        search_result = requests_url(url)

        # 用selenium
        # options.add_argument('--headless')
        # options.add_argument("--disable-javascript")
        # prefs = {"profile.managed_default_content_settings.images": 2,
        #          "profile.managed_default_content_settings.media_stream": 2,
        #          "profile.managed_default_content_settings.media_stream_mic": 2,
        #          "permissions.default.stylesheet": 2
        #          }
        # options.add_experimental_option("prefs", prefs)
        # driver = webdriver.Firefox(options=options)
        # driver.minimize_window()
        # driver.get(url)
        #
        # element = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.ID, 'content'))
        # )
        # driver.refresh()
        # search_result = driver.page_source
        soup = BeautifulSoup(search_result, 'html.parser')
        regular_table = soup.find('table', {'id': 'per_game'})
        offs_table = soup.find('table', {'id': 'playoffs_per_game'})
        totals = soup.find('table', {'id': 'totals'})
        playoffs_totals = soup.find('table', {'id': 'playoffs_totals'})
        all_salaries = soup.find('table', {'id': 'all_salaries'})
        salaries = {}
        regular_season_per_datas = []
        offs_table_per_datas = []
        regular_season_total_datas = []
        offs_table_total_datas = []

        if all_salaries:
            tbody = all_salaries.find('tbody')
            trs = tbody.find_all('tr')
            for tr in trs:
                key = tr.find_next('th').text
                sala = int(tr.find('td', {'data-stat': 'salary'}).get('csk', 0))
                if key not in salaries.keys():
                    salaries[key] = sala
                else:
                    salaries[key] += sala

        if regular_table:
            trs = regular_table.find_all('tr', class_='full_table')
            for tr in trs:
                season = tr.find_next('th').text
                team = tr.find('td', {'data-stat': 'team_id'}).text
                game_attend = int(tr.find('td', {'data-stat': 'g'}).text)
                try:
                    game_start = int(tr.find('td', {'data-stat': 'gs'}).text)
                except Exception:
                    game_start = 0
                minutes = float(tr.find('td', {'data-stat': 'mp_per_g'}).text)
                try:
                    pts = float(tr.find('td', {'data-stat': 'pts_per_g'}).text)
                except Exception:
                    pts = 0
                try:
                    oreb = float(tr.find('td', {'data-stat': 'orb_per_g'}).text)
                except Exception:
                    oreb = 0
                try:
                    dreb = float(tr.find('td', {'data-stat': 'drb_per_g'}).text)
                except Exception:
                    dreb = 0
                try:
                    reb = float(tr.find('td', {'data-stat': 'trb_per_g'}).text)
                except Exception:
                    reb = 0
                try:
                    ast = float(tr.find('td', {'data-stat': 'ast_per_g'}).text)
                except Exception:
                    ast = 0
                try:
                    fga = float(tr.find('td', {'data-stat': 'fga_per_g'}).text)
                except Exception:
                    fga = 0
                try:
                    fg = float(tr.find('td', {'data-stat': 'fg_per_g'}).text)
                except Exception:
                    fg = 0
                try:
                    fg3a = float(tr.find('td', {'data-stat': 'fg3a_per_g'}).text)
                except Exception:
                    fg3a = 0
                try:
                    fg3 = float(tr.find('td', {'data-stat': 'fg3_per_g'}).text)
                except Exception:
                    fg3 = 0
                try:
                    fta = float(tr.find('td', {'data-stat': 'fta_per_g'}).text)
                except Exception:
                    fta = 0
                try:
                    ft = float(tr.find('td', {'data-stat': 'ft_per_g'}).text)
                except Exception:
                    ft = 0
                try:
                    stl = float(tr.find('td', {'data-stat': 'stl_per_g'}).text)
                except Exception:
                    stl = 0
                try:
                    blk = float(tr.find('td', {'data-stat': 'blk_per_g'}).text)
                except Exception:
                    blk = 0
                try:
                    tov = float(tr.find('td', {'data-stat': 'tov_per_g'}).text)
                except Exception:
                    tov = 0
                regular_season_per_datas.append((
                    player_name, season, team, game_attend, game_start, minutes, pts, reb, oreb,
                    dreb, ast, fga, fg, fg3a, fg3, fta, ft, stl, blk, tov))
                print(f"{season}常规赛场均数据获取完毕")
                print(
                    f"选手：{player_id}，姓名：{player_name},上场时间：{minutes},母队：{team},是否上场：{game_attend}/{game_start}")
                print(
                    f"得分:{pts},篮板：{oreb}-{dreb}-{reb}，助攻：{ast}，投篮：{fg}/{fga}，三分球：{fg3}/{fg3a}，罚球：{ft}/{fta}，抢断：{stl}，盖帽：{blk}，失误：{tov}")
            regular_season_sql = """INSERT
                                INTO
                                public.player_regular_season
                                (
                                player_name, season, team, game_attend, game_start, minutes_average, pts, reb, oreb, dreb, ast, fga, fg,
                                fg3a, fg3, fta, ft, stl, blk, tov)
                                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            store_data_to_db(regular_season_sql, regular_season_per_datas)

        if offs_table:
            trs = offs_table.find_all('tr', class_='full_table')
            for tr in trs:
                season = tr.find_next('th').text
                team = tr.find('td', {'data-stat': 'team_id'}).text
                game_attend = int(tr.find('td', {'data-stat': 'g'}).text)
                try:
                    game_start = int(tr.find('td', {'data-stat': 'gs'}).text)
                except Exception:
                    game_start = 0
                minutes = float(tr.find('td', {'data-stat': 'mp_per_g'}).text)
                try:
                    pts = float(tr.find('td', {'data-stat': 'pts_per_g'}).text)
                except Exception:
                    pts = 0
                try:
                    oreb = float(tr.find('td', {'data-stat': 'orb_per_g'}).text)
                except Exception:
                    oreb = 0
                try:
                    dreb = float(tr.find('td', {'data-stat': 'drb_per_g'}).text)
                except Exception:
                    dreb = 0
                try:
                    reb = float(tr.find('td', {'data-stat': 'trb_per_g'}).text)
                except Exception:
                    reb = 0
                try:
                    ast = float(tr.find('td', {'data-stat': 'ast_per_g'}).text)
                except Exception:
                    ast = 0
                try:
                    fga = float(tr.find('td', {'data-stat': 'fga_per_g'}).text)
                except Exception:
                    fga = 0
                try:
                    fg = float(tr.find('td', {'data-stat': 'fg_per_g'}).text)
                except Exception:
                    fg = 0
                try:
                    fg3a = float(tr.find('td', {'data-stat': 'fg3a_per_g'}).text)
                except Exception:
                    fg3a = 0
                try:
                    fg3 = float(tr.find('td', {'data-stat': 'fg3_per_g'}).text)
                except Exception:
                    fg3 = 0
                try:
                    fta = float(tr.find('td', {'data-stat': 'fta_per_g'}).text)
                except Exception:
                    fta = 0
                try:
                    ft = float(tr.find('td', {'data-stat': 'ft_per_g'}).text)
                except Exception:
                    ft = 0
                try:
                    stl = float(tr.find('td', {'data-stat': 'stl_per_g'}).text)
                except Exception:
                    stl = 0
                try:
                    blk = float(tr.find('td', {'data-stat': 'blk_per_g'}).text)
                except Exception:
                    blk = 0
                try:
                    tov = float(tr.find('td', {'data-stat': 'tov_per_g'}).text)
                except Exception:
                    tov = 0
                print(f"{season}季后赛场均数据获取完毕")
                print(
                    f"选手：{player_id}，姓名：{player_name},上场时间：{minutes},母队：{team},是否上场：{game_attend}/{game_start}")
                print(
                    f"得分:{pts},篮板：{oreb}-{dreb}-{reb}，助攻：{ast}，投篮：{fg}/{fga}，三分球：{fg3}/{fg3a}，罚球：{ft}/{fta}，抢断：{stl}，盖帽：{blk}，失误：{tov}")
                offs_table_per_datas.append((
                    player_name, season, team, game_attend, game_start, minutes, pts, reb, oreb,
                    dreb, ast, fga, fg, fg3a, fg3, fta, ft, stl, blk, tov))
            offs_table_sql = """INSERT INTO public.player_playoffs_season
                                (player_name, season, team, game_attend, game_start, minutes_average, pts, reb, oreb, dreb, ast, fga, fg, fg3a, fg3, fta, ft, stl, blk, tov)
                                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                                                                """
            store_data_to_db(offs_table_sql, offs_table_per_datas)

        if totals:
            trs = totals.find_all('tr', class_='full_table')
            for tr in trs:
                season = tr.find_next('th').text
                salary = salaries.get(season)
                team = tr.find('td', {'data-stat': 'team_id'}).text
                game_attend = int(tr.find('td', {'data-stat': 'g'}).text)
                try:
                    game_start = int(tr.find('td', {'data-stat': 'gs'}).text)
                except Exception:
                    game_start = 0
                minutes = int(tr.find('td', {'data-stat': 'mp'}).text)
                try:
                    pts = int(tr.find('td', {'data-stat': 'pts'}).text)
                except Exception:
                    pts = 0
                try:
                    oreb = int(tr.find('td', {'data-stat': 'orb'}).text)
                except Exception:
                    oreb = 0
                try:
                    dreb = int(tr.find('td', {'data-stat': 'drb'}).text)
                except Exception:
                    dreb = 0
                try:
                    reb = int(tr.find('td', {'data-stat': 'trb'}).text)
                except Exception:
                    reb = 0
                try:
                    ast = int(tr.find('td', {'data-stat': 'ast'}).text)
                except Exception:
                    ast = 0
                try:
                    fga = int(tr.find('td', {'data-stat': 'fga'}).text)
                except Exception:
                    fga = 0
                try:
                    fg = int(tr.find('td', {'data-stat': 'fg'}).text)
                except Exception:
                    fg = 0
                try:
                    fg3a = int(tr.find('td', {'data-stat': 'fg3a'}).text)
                except Exception:
                    fg3a = 0
                try:
                    fg3 = int(tr.find('td', {'data-stat': 'fg3'}).text)
                except Exception:
                    fg3 = 0
                try:
                    fta = int(tr.find('td', {'data-stat': 'fta'}).text)
                except Exception:
                    fta = 0
                try:
                    ft = int(tr.find('td', {'data-stat': 'ft'}).text)
                except Exception:
                    ft = 0
                try:
                    stl = int(tr.find('td', {'data-stat': 'stl'}).text)
                except Exception:
                    stl = 0
                try:
                    blk = int(tr.find('td', {'data-stat': 'blk'}).text)
                except Exception:
                    blk = 0
                try:
                    tov = int(tr.find('td', {'data-stat': 'tov'}).text)
                except Exception:
                    tov = 0
                try:
                    triple = int(tr.find('td', {'data-stat': 'trp_dbl'}).text)
                except Exception:
                    triple = 0
                print(f"{season}常规赛总数据获取完毕")
                print(
                    f"选手：{player_id}，姓名：{player_name},上场时间：{minutes},母队：{team},是否上场：{game_attend}/{game_start},薪水：{salary}")
                print(
                    f"得分:{pts},篮板：{oreb}-{dreb}-{reb}，助攻：{ast}，投篮：{fg}/{fga}，三分球：{fg3}/{fg3a}，罚球：{ft}/{fta}，抢断：{stl}，盖帽：{blk}，失误：{tov}")
                regular_season_total_datas.append(
                    (player_name, season, team, game_attend, game_start, minutes, pts, reb, oreb,
                     dreb, ast, fga, fg, fg3a, fg3, fta, ft, stl, blk, tov, triple, salary, player_url))
            regular_total_sql = """INSERT INTO public.player_regular_total_season
                                    (player_name, season, team, game_attend, game_start, minutes_attend, pts, reb, oreb, dreb, ast, fga, fg, fg3a, fg3, fta, ft, stl, blk, tov, triple, salary, href)
                                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s);
                                    """
            store_data_to_db(regular_total_sql, regular_season_total_datas)
        if playoffs_totals:
            trs = playoffs_totals.find_all('tr', class_='full_table')
            for tr in trs:
                season = tr.find_next('th').text
                team = tr.find('td', {'data-stat': 'team_id'}).text
                game_attend = int(tr.find('td', {'data-stat': 'g'}).text)
                try:
                    game_start = int(tr.find('td', {'data-stat': 'gs'}).text)
                except Exception:
                    game_start = 0
                minutes = int(tr.find('td', {'data-stat': 'mp'}).text)
                try:
                    pts = int(tr.find('td', {'data-stat': 'pts'}).text)
                except Exception:
                    pts = 0
                try:
                    oreb = int(tr.find('td', {'data-stat': 'orb'}).text)
                except Exception:
                    oreb = 0
                try:
                    dreb = int(tr.find('td', {'data-stat': 'drb'}).text)
                except Exception:
                    dreb = 0
                try:
                    reb = int(tr.find('td', {'data-stat': 'trb'}).text)
                except Exception:
                    reb = 0
                try:
                    ast = int(tr.find('td', {'data-stat': 'ast'}).text)
                except Exception:
                    ast = 0
                try:
                    fga = int(tr.find('td', {'data-stat': 'fga'}).text)
                except Exception:
                    fga = 0
                try:
                    fg = int(tr.find('td', {'data-stat': 'fg'}).text)
                except Exception:
                    fg = 0
                try:
                    fg3a = int(tr.find('td', {'data-stat': 'fg3a'}).text)
                except Exception:
                    fg3a = 0
                try:
                    fg3 = int(tr.find('td', {'data-stat': 'fg3'}).text)
                except Exception:
                    fg3 = 0
                try:
                    fta = int(tr.find('td', {'data-stat': 'fta'}).text)
                except Exception:
                    fta = 0
                try:
                    ft = int(tr.find('td', {'data-stat': 'ft'}).text)
                except Exception:
                    ft = 0
                try:
                    stl = int(tr.find('td', {'data-stat': 'stl'}).text)
                except Exception:
                    stl = 0
                try:
                    blk = int(tr.find('td', {'data-stat': 'blk'}).text)
                except Exception:
                    blk = 0
                try:
                    tov = int(tr.find('td', {'data-stat': 'tov'}).text)
                except Exception:
                    tov = 0
                print(f"{season}季后赛总数据获取完毕")
                print(
                    f"选手：{player_id}，姓名：{player_name},上场时间：{minutes},母队：{team},是否上场：{game_attend}/{game_start}")
                print(
                    f"得分:{pts},篮板：{oreb}-{dreb}-{reb}，助攻：{ast}，投篮：{fg}/{fga}，三分球：{fg3}/{fg3a}，罚球：{ft}/{fta}，抢断：{stl}，盖帽：{blk}，失误：{tov}")
                offs_table_total_datas.append((
                    player_name, season, team, game_attend, game_start, minutes, pts, reb, oreb,
                    dreb, ast, fga, fg, fg3a, fg3, fta, ft, stl, blk, tov))
            playoffs_totals_sql = """INSERT INTO public.player_playoffs_total_season
                                    (player_name, season, team, game_attend, game_start, minutes_attend, pts, reb, oreb, dreb, ast, fga, fg, fg3a, fg3, fta, ft, stl, blk, tov)
                                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                                    """
            store_data_to_db(playoffs_totals_sql, offs_table_total_datas)
        # driver.quit()
        random_number = random.randint(7, 13)
        time.sleep(random_number)
