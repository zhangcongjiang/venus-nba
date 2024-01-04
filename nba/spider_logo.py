import os
import time

import requests

from nba.constants import nba_teams
from tools.sqlUtils import get_sql
from nba.constants import nba_teams

destination_folder = "F:\\pycharm_workspace\\venus\\nba\\logo"

players = get_sql("select * from public.player_active where id>526  and player_id is not  null order by id;")

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'acw_tc=0bdd346216970285458832633eae5694b1df7212045652e18fe1d946a4e2ae; i18next=zh_CN; locale=zh_CN; countryCode=CN; sajssdk_2015_cross_new_user=1; privacyV2=true; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218b1ec8a95e80-0d488d073be8ae8-26031e51-1327104-18b1ec8a95f12c5%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThiMWVjOGE5NWU4MC0wZDQ4OGQwNzNiZThhZTgtMjYwMzFlNTEtMTMyNzEwNC0xOGIxZWM4YTk1ZjEyYzUifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218b1ec8a95e80-0d488d073be8ae8-26031e51-1327104-18b1ec8a95f12c5%22%7D',
    'If-None-Match': '"10026-1c17bef8a63b7454a86f96bc0af10df2f5e4d2cf"',
    'Referer': 'http://china.nba.cn/players/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}
for player in players:
    player_name = player.get('player_name').replace(" ", "_").replace("'", "").replace("-", "_")
    player_id = player.get('player_id')
    head_url = f"https://res.nba.cn/media/img/players/head/260x190/{player_id}.png"

    body_url = f"https://res.nba.cn/media/img/players/silos/440x700/{player_id}.png"
    response = requests.get(head_url, headers=headers, verify=False)

    new_filename = os.path.join(destination_folder, f"{player_name}_head.png")
    if response.status_code == 200:
        with open(new_filename, 'wb') as f:
            f.write(response.content)
            print(f"{player.get('id')}，图片已成功下载并保存为: {new_filename}")
    else:
        print("未找到图片：", player_name)
    time.sleep(3)
