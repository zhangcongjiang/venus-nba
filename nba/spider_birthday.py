import random

import requests
from bs4 import BeautifulSoup
import time

from tools.sqlUtils import update_signal, get_sql


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


if __name__ == '__main__':
    # sql = """SELECT id,player_name,href FROM public.player_active where id >510 and  birthday IS NULL and href !='' ORDER BY id;"""
    # players = get_sql(sql)

    # for player in players:
    #     print(player)
    #     player_name = player.get('player_name')
    #     player_url = player.get('href')
    #     player_id = player.get('id')

        # url = f"https://www.basketball-reference.com{player_url}"
    url = "https://www.basketball-reference.com/players/j/jamesle01.html"
    # 用requests方法
    search_result = requests_url(url)

    soup = BeautifulSoup(search_result, 'html.parser')

    all_star = soup.find("div", {'id', "leaderboard_allstar"})
    trs = all_star.find_all("tr")
    for tr in trs:
        print(tr.get_text())
    # birth = soup.find("span", {'id': 'necro-birth'}).get('data-birth')
    # print(f"player id {player_id},birthday:{birth}")
    # update_sql = f"""update public.player_active set birthday = %s where id=%s;"""
    # update_signal(update_sql, (birth, player_id))

        # random_number = random.randint(5, 10)
        # time.sleep(random_number)
