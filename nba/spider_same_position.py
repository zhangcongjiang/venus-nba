# -*- coding: utf-8 -*-
from datetime import datetime, date

import requests

from nba.constants import nba_teams
from nba.image_utils import ImageUtils
from nba.nba_utils import get_player_last_season_data, get_game_data
from nba.sqlUtils import store_to_db, get_sql


def same_position():
    sql = """select player_name, draft_year, team,chinese_name,code  from public.player_draft where draft_position =1 and draft_year >=2000;"""
    players = get_sql(sql)
    datas = []
    for p in players:
        print(p)
        sql = f"""SELECT id, player_name, season, game_date, up, playing_time, pts, reb, oreb, dreb, ast, fga, fg, fg3a, fg3, fta, ft, stl, blk, tov, plus_minus, team, opp, game_win FROM public.player_regular_gamelog where player_name ='{p.get('player_name')}' and up=True order by  game_date  limit 5 ;
                            """
        first_data = get_game_data(sql)
        first_data['player_name'] = p.get('player_name')
        first_data['draft_year'] = p.get('draft_year')
        first_data['chinese_name'] = p.get('chinese_name')
        first_data['code'] = p.get('code')
        first_data['team'] = nba_teams.get(p.get('team'))
        datas.append(first_data)
    sorted_datas = sorted(datas, key=lambda x: x['score'] + x['win'], reverse=True)
    today = datetime.now().strftime("%Y-%m-%d")
    tag = 'first_game'
    file_name = f"F:\\notebooks\\其他\\draft\\{today}_first_game.md"
    with open(file_name, "w", encoding="utf-8") as file:
        i = 0
        for p in sorted_datas:
            i += 1
            file.write(f"#### 第{i}位. {p.get('draft_year')}-{p.get('team')}-**{p.get('chinese_name')}**\n\n")
            pd_str = ImageUtils().format_draw_data(p.get('code'), tag, p.get('hit_rate').replace("，", " | "),
                                                   p.get('data'))
            file.write(
                f"![{p.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{p.get('code')}_{tag}.png)\n\n")

            print({p.get('player_name')}, p)
            file.write(f"战绩：{p.get('win')}胜{p.get('loss')}负\n\n")
            file.write(f"数据：**{pd_str}**\n\n")
            file.write(f"命中率：{p.get('hit_rate')}\n\n")

            file.write("---\n\n")


def player_list():
    big_contract = [
        {
            'player_name': 'jakob_poeltl',
            'contract': "4年8000万美金",
            'name': '雅各布·珀尔特尔',
            'team': "猛龙",
            'activity': False,
        },
        {
            'player_name': 'josh_hart',
            'contract': "4年8100万美金",
            'name': '约什·哈特',
            'team': "尼克斯",
            'activity': False,
        },
        {
            'player_name': 'dillon_brooks',
            'contract': "4年8600万美金",
            'name': '狄龙·布鲁克斯',
            'team': "火箭",
            'activity': False,
        },
        {
            'player_name': 'draymond_green',
            'contract': "4年1亿美金",
            'name': '德雷蒙德·格林',
            'team': "勇士",
            'activity': False,
        },
        {
            'player_name': 'kyle_kuzma',
            'contract': "4年1.02亿美金",
            'name': '凯尔·库兹马',
            'team': "奇才",
            'activity': False,
        },
        {
            'player_name': 'khris_middleton',
            'contract': "3年1.02亿美金",
            'name': '克里斯·米德尔顿',
            'team': "雄鹿",
            'activity': False,
        },
        {
            'player_name': 'cameron_johnson',
            'contract': "4年1.08亿美金",
            'name': '卡梅伦·约翰逊',
            'team': "篮网",
            'activity': False,
        },
        {
            'player_name': 'dejounte_murray',
            'contract': "4年1.2亿美金",
            'name': '德章泰·默里',
            'team': "老鹰",
            'activity': False,
        },
        {
            'player_name': 'kyrie_irving',
            'contract': "3年1.26亿美金",
            'name': '凯里·欧文',
            'team': "独行侠",
            'activity': False,
        },
        {
            'player_name': 'fred_vanvleet',
            'contract': "3年1.3亿美金",
            'name': '弗雷德·范弗利特',
            'team': "火箭",
            'activity': False,
        },
        {
            'player_name': 'jaden_mcdaniels',
            'contract': "5年1.36亿美金",
            'name': '杰登·麦克丹尼尔斯',
            'team': "森林狼",
            'activity': False,
        },
        {
            'player_name': 'devin_vassell',
            'contract': "5年1.46亿美金",
            'name': '德文·瓦塞尔',
            'team': "马刺",
            'activity': False,
        },
        {
            'player_name': 'jerami_grant',
            'contract': "5年1.6亿美金",
            'name': '杰拉米·格兰特',
            'team': "开拓者",
            'activity': False,
        },
        {
            'player_name': 'giannis_antetokounmpo',
            'contract': "3年1.86亿美金",
            'name': '扬尼斯·阿德托昆博',
            'team': "雄鹿",
            'activity': False,
        },
        {
            'player_name': 'anthony_davis',
            'contract': "3年1.86亿美金",
            'name': '安东尼·戴维斯',
            'team': "湖人",
            'activity': False,
        },
        {
            'player_name': 'desmond_bane',
            'contract': "5年2.07亿美金",
            'name': '戴斯蒙德·贝恩',
            'team': "雄鹿",
            'activity': False,
        },
        {
            'player_name': 'domantas_sabonis',
            'contract': "5年2.17亿美金",
            'name': '多曼塔斯·萨博尼斯',
            'team': "国王",
            'activity': False,
        },
        {
            'player_name': 'tyrese_haliburton',
            'contract': "5年2.6亿美金",
            'name': '泰瑞斯·哈利伯顿',
            'team': "步行者",
            'activity': False,
        },
        {
            'player_name': 'lamelo_ball',
            'contract': "5年2.6亿美金",
            'name': '拉梅洛·鲍尔',
            'team': "黄蜂",
            'activity': False,
        },
        {
            'player_name': 'anthony_edwards',
            'contract': "5年2.6亿美金",
            'name': '安东尼·爱德华兹',
            'team': "森林狼",
            'activity': False,
        },
        {
            'player_name': 'jaylen_brown',
            'contract': "5年3.04亿美金",
            'name': '杰伦·布朗',
            'team': "凯尔特人",
            'activity': False,
        },
    ]
    datas = []
    for p in big_contract:
        player_name = \
            get_sql(f"""select player_name from public.player_active where code = '{p.get('player_name')}'""")[0].get(
                'player_name')
        sql = f"""SELECT id, player_name, season, game_date, up, playing_time, pts, reb, oreb, dreb, ast, fga, fg, fg3a, fg3, fta, ft, stl, blk, tov, plus_minus, team, opp, game_win FROM public.player_regular_gamelog where player_name ='{player_name}' and up=True and season=2024 ;
                            """
        data = get_game_data(sql)
        data['contract'] = p.get('contract')
        data['team'] = p.get('team')
        data['name'] = p.get('name')
        data['code'] = p.get('player_name')
        datas.append(data)
    sorted_datas = sorted(datas, key=lambda x: x['score'] + x['win'], reverse=True)
    today = datetime.now().strftime("%Y-%m-%d")
    tag = 'big_contract'
    file_name = f"F:\\notebooks\\其他\\draft\\{today}_big_contract.md"
    with open(file_name, "w", encoding="utf-8") as file:
        i = 0
        for p in sorted_datas:
            i += 1
            file.write(f"#### {i}. {p.get('team')}-{p.get('name')}\n\n")
            pd_str = ImageUtils().format_draw_data(p.get('code'), tag, p.get('hit_rate').replace("，", " | "),
                                                   p.get('data'))
            file.write(
                f"![{p.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{p.get('code')}_{tag}.png)\n\n")

            print({p.get('player_name')}, p)
            file.write(f"战绩：{p.get('win')}胜{p.get('loss')}负\n\n")
            file.write(f"合同：{p.get('contract')}\n\n")
            file.write(f"数据：**{pd_str}**\n\n")
            file.write(f"命中率：{p.get('hit_rate')}\n\n")

            file.write("---\n")


if __name__ == '__main__':
    player_list()