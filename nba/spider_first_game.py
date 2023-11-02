# -*- coding: utf-8 -*-
from datetime import datetime, date

import requests

from nba.constants import nba_teams
from nba.nba_utils import get_player_last_season_data, get_game_data
from nba.sqlUtils import store_to_db, get_sql

if __name__ == '__main__':
    sql = """select player_name, draft_year, team,chinese_name,code  from public.player_draft where draft_position =3 and draft_year >=2000 and draft_year <2023 ;"""
    players = get_sql(sql)
    datas = []
    for p in players:
        print(p)
        first_data = get_game_data(p.get('player_name'))
        first_data['player_name'] = p.get('player_name')
        first_data['draft_year'] = p.get('draft_year')
        first_data['chinese_name'] = p.get('chinese_name')
        first_data['code'] = p.get('code')
        datas.append(first_data)
    datas.append({
        'player_name': 'Scoot Henderson',
        'chinese_name': '斯库特·亨德森',
        'code': 'scoot_henderson',
        'sum': 18,
        'team': '开拓者',
        'opp': '快船',
        'game_date': "2023-10-26",
        'draft_year': 2023,
        'attend': '35:50',
        'data': '**11分 | 3篮板 | 4助攻 | 4失误**',
        'hit_rate': '5/11 | 三分球：0/3 | 罚球：1/1'
    })
    sorted_datas = sorted(datas, key=lambda x: x['sum'])
    today = datetime.now().strftime("%Y-%m-%d")
    file_name = f"F:\\notebooks\\其他\\draft\\{today}_first_game.md"
    with open(file_name, "w", encoding="utf-8") as file:
        i = 25
        for p in sorted_datas:
            i -= 1
            file.write(f"#### 第{i}位. {p.get('draft_year')}-{p.get('team')}-**{p.get('chinese_name')}**\n\n")

            print({p.get('player_name')}, p)
            file.write(f"比赛日期：{p.get('game_date')} 对阵 {p.get('opp')}\n\n")
            file.write(f"上场时间：{p.get('attend')}\n\n")
            file.write(f"数据：{p.get('data')}\n\n")
            file.write(f"命中率：{p.get('hit_rate')}\n\n")
            file.write(
                f"![{p.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\img\\{p.get('code')}.png)\n\n")

            file.write("---\n\n")
