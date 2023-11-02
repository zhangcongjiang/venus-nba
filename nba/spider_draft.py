import datetime

import requests
from bs4 import BeautifulSoup
import time

# from collector.database import PsqlConnect
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import psycopg2
from selenium.webdriver.support.wait import WebDriverWait
from settings import REDIS_DATA_TIMEOUT
from tools.redis_tools import ControlRedis


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


def request_statics(response, name, draft_year):
    # 使用Beautiful Soup解析HTML
    soup = BeautifulSoup(response, 'html.parser')
    # 使用find方法查找具有id="pgl_basic"的表格
    try:
        table = soup.find('table', {'id': 'pgl_basic'})
        season = table.find_previous('h2').get_text().split(" ")[0]
    except Exception:
        return

    # print(season)
    data = []
    # 检查是否找到表格
    if table:
        tbody = table.find('tbody')
        tr_tags = tbody.find_all('tr')
        for tr in tr_tags:
            if tr.get('class') and 'thead' in tr.get('class'):
                continue
            date_game = tr.find('td', {'data-stat': 'date_game'}).text
            team = tr.find('td', {'data-stat': 'team_id'}).text
            opp = tr.find('td', {'data-stat': 'opp_id'}).text
            # game_id = tr.find('th', {'data-stat': 'ranker'}).text
            game_result = tr.find('td', {'data-stat': 'game_result'}).text
            game_win = True if game_result.split(" ")[0] == 'W' else False
            if tr.get('id') and tr.get('id').startswith('pgl_basic.'):
                up = True
                playing_time = tr.find('td', {'data-stat': 'mp'}).text
                split_playing_time = playing_time.split(":")
                try:
                    format_playing_time = f"{split_playing_time[0]} minutes {split_playing_time[1]} seconds"
                except Exception:
                    format_playing_time = '0 minutes 0 seconds'
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
                    plus_minus = int(tr.find('td', {'data-stat': 'plus_minus'}).text)
                except Exception:
                    plus_minus = 0

            else:
                up = False
                format_playing_time = '0 minutes 0 seconds'
                pts = oreb = dreb = reb = ast = fg = fga = fg3 = fg3a = ft = fta = stl = blk = tov = plus_minus = 0
            data.append((name, season, draft_year, date_game, up, format_playing_time, pts, reb, oreb,
                         dreb, ast, fga, fg, fg3a, fg3, fta, ft, stl, blk, tov, plus_minus,
                         team, opp, game_win))
            # print(f"{season}赛季数据获取完毕")
            # print(
            #     f"日期:{date_game},选手：{player_name},上场时间：{format_playing_time},母队：{team},对手：{opp},game_id:{game_id},是否上场：{up}")
            # print(
            #     f"得分:{pts},篮板：{oreb}-{dreb}-{reb}，助攻：{ast}，投篮：{fg}/{fga}，三分球：{fg3}/{fg3a}，罚球：{ft}/{fta}，抢断：{stl}，盖帽：{blk}，失误：{tov}，正负值：{plus_minus}")
    else:
        print("Table with id='pgl_basic' not found on the page")
    # print(f"{season}赛季数据获取完毕")
    if data:
        store_draft_info_db(data)


def store_draft_info_db(data):
    # 连接到数据库
    psql = PsqlConnect()
    conn = psql.connect(host="10.67.0.165",
                        database="spider",
                        user="postgres",
                        password="postgres",
                        port="5432")

    print(data)
    sql = f"""INSERT INTO public.player_draft ("player_name", "draft_year","draft_position","team", "href","attend")
            VALUES (%s, %s, %s, %s, %s,%s)
            ON CONFLICT DO NOTHING;
            """

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


def get_user_info(url):
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        ths = soup.find_all('th', class_='left')
        datas = []
        for th in ths:
            name = th.find_next("a").text
            ulr_path = th.get('data-append-csv')
            start_year = th.find_next('td').text
            end_year = th.find_next('td').find_next('td').text
            # print(f"name:{name},url_path:{ulr_path},start_year:{start_year},end_year:{end_year}")
            datas.append({
                "name": name,
                "url_path": ulr_path,
                "start_year": int(start_year),
                "end_year": int(end_year),
            })
        return datas


if __name__ == '__main__':

    for year in range(2023, 1980, -1):
        data = []
        url = f"https://www.basketball-reference.com/draft/NBA_{year}.html"
        # chrome_options = Options()
        driver = webdriver.Firefox()
        driver.minimize_window()
        driver.get(url)
        search_result = driver.page_source
        soup = BeautifulSoup(search_result, 'html.parser')

        # for alphabet in range(ord('e'), ord('z') + 1):
        #     url = f"https://www.basketball-reference.com/players/{chr(alphabet)}/"
        #     chrome_options = Options()
        #     # chrome_options.add_argument('--headless')
        #     # chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')
        #     # chrome_options.add_argument('--disable-gpu')
        #     driver = webdriver.Chrome(options=chrome_options)
        #     driver.minimize_window()
        #     driver.get(url)
        #     search_result = driver.page_source
        #     soup = BeautifulSoup(search_result, 'html.parser')
        table = soup.find('table', {'id': 'stats'})
        trs = table.find_all('tr')
        for tr in trs:
            try:
                rank = tr.find('td', {'data-stat': 'pick_overall'}).text
                name = tr.find('td', {'data-stat': 'player'})
                team = tr.find('td', {'data-stat': 'team_id'}).text
                detail_url = name.find_next('a').get('href')
                seasons = tr.find('td', {'data-stat': 'seasons'}).text
                attend = True if seasons else False

                print(name.text, year, rank, team, detail_url, attend)
                data.append((name.text, year, rank, team, detail_url, attend))

            except Exception:
                pass
        store_draft_info_db(data)

        # players = []
        # for th in ths:
        #     name = th.find_next("a").text
        #     ulr_path = th.get('data-append-csv')
        #     start_year = th.find_next('td').text
        #     end_year = th.find_next('td').find_next('td').text
        #     # print(f"name:{name},url_path:{ulr_path},start_year:{start_year},end_year:{end_year}")
        #     players.append({
        #         "name": name,
        #         "url_path": ulr_path,
        #         "start_year": int(start_year),
        #         "end_year": int(end_year),
        #     })
        # go_on = True
        #
        # for player in players:
        #     print(f"player:{player.get('name')}")
        #     # if player.get('name') == "Jerome Dyson":
        #     #     player["start_year"] = 2013
        #     #     go_on = True
        #     if go_on:
        #         # 指定要爬取的网页URL
        #         for year in range(player.get("start_year"), player.get("end_year") + 1):
        #             draft_year = player.get("start_year") - 1
        #             if draft_year >= 1984:
        #                 player_url = f"https://www.basketball-reference.com/players/c/{player.get('url_path')}/gamelog/{year}"
        #                 driver.execute_script(
        #                     f"window.open('{player_url}', '_blank');")
        #                 driver.minimize_window()
        #                 driver.switch_to.window(driver.window_handles[1])
        #                 # driver.refresh()
        #                 response = driver.page_source
        #                 request_statics(response, player.get("name"), draft_year)
        #                 print(f"player {player.get('name')} {year} ok")
        #                 driver.close()
        #                 driver.switch_to.window(driver.window_handles[0])
        #                 time.sleep(2)
        #         time.sleep(1)
        driver.quit()
        time.sleep(1)
