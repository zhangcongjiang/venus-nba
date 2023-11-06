# -*- coding: utf-8 -*-
from datetime import datetime, date

import requests

from nba.constants import nba_teams
import nba.nba_utils
from nba.image_utils import ImageUtils
from nba.nba_utils import get_player_last_season_data, get_person_info
from nba.sqlUtils import store_to_db, get_sql

if __name__ == '__main__':

    usa_players = ['Paolo Banchero', 'Austin Reaves', 'Josh Hart', 'Cameron Johnson', 'Walker Kessler', 'Mikal Bridges',
                   'Anthony Edwards', 'Tyrese Haliburton', 'Brandon Ingram', 'Jaren Jackson Jr.', 'Bobby Portis',
                   'Jalen Brunson']
    players = get_sql("select player_name from public.player_active where draft_year <2009 ;")
    players = get_sql(
        "SELECT player_name FROM public.player_regular_gamelog WHERE season=2024 GROUP BY player_name HAVING SUM(fg3a) > 10 and (SUM(fg3) / SUM(fg3a::float)) < 0.2;")

    players = [player.get('player_name') for player in players]
    datas = []
    tag = "fg3a"
    for p in players:
        data = get_person_info(p.replace("'", "''"))

        datas.append(data)

    sorted_datas = sorted(datas, key=lambda x: x['this_score'], reverse=True)
    today = datetime.now().strftime("%Y-%m-%d")
    file_name = f"F:\\notebooks\\其他\\draft\\{today}_{tag}.md"
    with open(file_name, "w", encoding="utf-8") as file:
        i = 20
        for data in reversed(sorted_datas):
            # if data['this_score'] < 10:
            #     continue
            i -= 1

            print(data)
            file.write(f"#### {i}：**{data.get('this_team')}-{data.get('chinese_name')}**\n\n")
            file.write(f"原选秀：**{data.get('draft_year')}**年第**{data.get('draft_position')}**顺位\n\n")
            ImageUtils().draw_text(data.get('code'), tag, data.get('this_hit_rate').replace("，", " | "), (
                '┏',
                '得分：', f"{data.get('this_data')[0]}",
                '篮板：', f"{data.get('this_data')[1]}",
                '助攻；', f"{data.get('this_data')[2]}",
                '抢断：', f"{data.get('this_data')[3]}",
                '盖帽：', f"{data.get('this_data')[4]}",
                '┛'))
            file.write(
                f"![{data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{data.get('code')}_{tag}.png)\n\n")
            file.write(
                f"本赛季已经代表{data.get('this_team')}出战{data.get('this_attend')}场比赛，取得{data.get('this_win')}胜{data.get('this_loss')}负的战绩\n\n")
            file.write(
                f"本赛季数据：**{data.get('this_data')[0]}分 | {data.get('this_data')[1]}篮板 | {data.get('this_data')[2]}助攻 | {data.get('this_data')[3]}抢断 | {data.get('this_data')[4]}盖帽**\n\n")
            file.write(f"命中率：{data.get('this_hit_rate')}\n\n")
            # file.write(f"上赛季数据：**{data.get('last_data')}**\n\n")
            file.write("---\n\n")
