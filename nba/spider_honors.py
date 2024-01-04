import re
from datetime import datetime
import random

import requests
from bs4 import BeautifulSoup, Comment
import time

from tools.nba_utils import NbaUtils
from tools.sqlUtils import update_signal, get_sql, store_to_db

nba_utils = NbaUtils()


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


def handle_contract(player_name, contract):
    data = []
    if contract:
        keys = contract.find_all('th')
        values = contract.find_all('td')
        for i in range(1, len(keys)):
            year = keys[i].get('data-stat')
            season = int(year.split('-')[0]) + 1
            salary = int(values[i].text.replace("$", "").replace(",", ""))
            data.append((player_name, season, salary))
    if data:
        sql = f"""INSERT INTO public.player_salary ("player_name", "season","salary")
            VALUES (%s, %s,%s)
            ON CONFLICT DO NOTHING;
            """

        store_to_db(sql, data)


def handle_honor(honor):
    maps = {
        "All Star": "全明星",
        "Scoring Champ": "得分王",
        "AST Champ": "助攻王",
        "STL Champ": "抢断王",
        "BLK Champ": "盖帽王",
        "TRB Champ": "篮板王",
        "Def. POY": "最佳防守球员",
        "NBA Champ": "总冠军",
        "All-NBA": "最佳阵容",
        "ROY": "最佳新秀",
        "AS MVP": "全明星赛MVP",
        "All-Defensive": "最佳防守阵容",
        "Finals MVP": "FMVP",
        "Sixth Man": "最佳第六人",
        "Most Improved": "进步最快球员",
        "All-Rookie": "最佳新秀阵容"
    }
    for key in maps.keys():
        if key in honor:
            honor = honor.replace(key, maps.get(key))
    return honor


def month_to_number(month):
    month_dict = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12
    }
    return month_dict.get(month, None)


if __name__ == '__main__':
    sql = """SELECT id,player_name,href FROM public.player_draft where  id>=63 and attend=TRUE order by id;"""
    players = get_sql(sql)
    for player in players:
        print(player)
        player_name = player.get('player_name')
        player_url = player.get('href')
        player_id = player.get('id')

        url = f"https://www.basketball-reference.com{player_url}"
        # url = "https://www.basketball-reference.com/players/j/jamesle01.html"
        # 用requests方法
        search_result = requests_url(url)
        soup = BeautifulSoup(search_result, 'html.parser')

        honor_ul = soup.find('ul', {'id': 'bling'})
        if not honor_ul:
            continue
        lis = honor_ul.find_all('li')
        honors = []
        for li in lis:
            honor = li.get_text()
            honors.append((player_name, handle_honor(honor)))

        if honors:
            print(honors)
            sql = f"""INSERT INTO public.player_honors (player_name, honor)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
                """

            store_to_db(sql, honors)
            random_number = random.randint(7, 13)
            time.sleep(random_number)
