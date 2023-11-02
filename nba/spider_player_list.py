# -*- coding: utf-8 -*-
from datetime import datetime, date

import requests

from nba.constants import nba_teams
import nba.nba_utils
from nba.nba_utils import get_player_last_season_data, get_person_info
from nba.sqlUtils import store_to_db, get_sql

if __name__ == '__main__':

    usa_players = ['Paolo Banchero', 'Austin Reaves', 'Josh Hart', 'Cameron Johnson', 'Walker Kessler', 'Mikal Bridges',
                   'Anthony Edwards', 'Tyrese Haliburton', 'Brandon Ingram', 'Jaren Jackson Jr.', 'Bobby Portis',
                   'Jalen Brunson']
    # players = get_sql("select player_name from public.player_active where draft_year =2021;")
    # players = [player.get('player_name') for player in players]
    datas = []
    for p in usa_players:
        data = get_person_info(p.replace("'", "''"))
        if data['this_score'] and data['last_score']:
            datas.append(data)

    sorted_datas = sorted(datas, key=lambda x: x['this_score'] - x['last_score'], reverse=True)
    today = datetime.now().strftime("%Y-%m-%d")
    file_name = f"F:\\notebooks\\其他\\draft\\{today}_usa.md"
    with open(file_name, "w", encoding="utf-8") as file:
        i = 19
        for data in reversed(sorted_datas):
            if data['this_score'] < 12:
                continue
            i -= 1

            print(data)
            file.write(f"#### 第{i}顺位：**{data.get('this_team')}-{data.get('chinese_name')}**\n\n")
            file.write(f"原选秀：**{data.get('draft_year')}**年第**{data.get('draft_position')}**顺位\n\n")
            file.write(
                f"![{data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\image\\{data.get('code')}.png)\n\n")
            file.write(
                f"本赛季已经代表{data.get('this_team')}出战{data.get('this_attend')}场比赛，取得{data.get('this_win')}胜{data.get('this_loss')}负的战绩\n\n")
            file.write(f"本赛季数据：**{data.get('this_data')}**\n\n")
            file.write(f"命中率：{data.get('this_hit_rate')}\n\n")
            file.write("---\n\n")
            file.write(f"上赛季数据：**{data.get('last_data')}**\n\n")
            file.write(f"命中率：{data.get('last_hit_rate')}\n\n")

            file.write("---\n\n")
