import datetime
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


# if __name__ == '__main__':
#     sql = """SELECT id,player_name,href FROM public.player_active where  id>0  ORDER BY id;"""
#     players = get_sql(sql)
#     exists = get_sql("SELECT DISTINCT player_name FROM public.player_salary;")
#     exist_players = []
#     for p in exists:
#         exist_players.append(p.get('player_name'))
#     for player in players:
#         print(player)
#         player_name = player.get('player_name')
#         if player_name in exist_players:
#             continue
#         player_url = player.get('href')
#         player_id = player.get('id')
#
#         url = f"https://www.basketball-reference.com{player_url}"
#         # 用requests方法
#         search_result = requests_url(url)
#
#         soup = BeautifulSoup(search_result, 'html.parser')
#         if soup.find('div', {'id': 'div_contract'}):
#             contract_table = soup.find('div', {'id': 'div_contract'}).find('table', class_='suppress_all')
#             handle_contract(player_name, contract_table)
#
#         else:
#             # 找到所有注释
#             comments = soup.find_all(string=lambda text: isinstance(text, Comment))
#             comment_contents = []  # 保存注释内容的列表
#             for comment in comments:
#                 comment_contents.append(comment)
#
#             for com in comment_contents:
#                 comment_soup = BeautifulSoup(com, 'html.parser')
#                 if comment_soup.find('div', {'id': 'div_contract'}):
#                     contract_table = comment_soup.find('div', {'id': 'div_contract'}).find('table', class_='suppress_all')
#                     handle_contract(player_name, contract_table)
#
#         random_number = random.randint(15, 20)
#         time.sleep(random_number)

if __name__ == '__main__':
    sql = """SELECT id,player_name,href FROM public.player_draft where  id>=0"""
    players = get_sql(sql)
    for player in players:
        print(player)
        player_name = player.get('player_name')
        player_url = player.get('href')
        player_id = player.get('id')

        url = f"https://www.basketball-reference.com{player_url}"
        # 用requests方法
        search_result = requests_url(url)
        soup = BeautifulSoup(search_result, 'html.parser')

        all_salaries = soup.find('table', {'id': 'all_salaries'})

        if not all_salaries:
            # 找到所有注释
            comments = soup.find_all(string=lambda text: isinstance(text, Comment))
            comment_contents = []  # 保存注释内容的列表
            for comment in comments:
                comment_contents.append(comment)

            for com in comment_contents:
                comment_soup = BeautifulSoup(com, 'html.parser')
                if comment_soup.find('div', {'id': 'all_salaries'}):
                    all_salaries = comment_soup.find('div', {'id': 'all_salaries'})

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
            data = []
            for k, v in salaries.items():
                data.append((player_name, k, v))

            print(data)

        random_number = random.randint(7, 13)
        time.sleep(random_number)
