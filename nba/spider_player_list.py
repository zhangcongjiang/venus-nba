# -*- coding: utf-8 -*-
import os
from datetime import datetime

from nba.image_utils import ImageUtils
from nba.nba_utils import NbaUtils
from nba.sqlUtils import get_sql

nba_utils = NbaUtils()
today = datetime.now().strftime("%Y-%m-%d")
file_path = "F:\\notebooks\\其他\\draft"


def best_season(players, tag):
    file_name = os.path.join(file_path, f"{today}_{tag}")
    with open(file_name, "w", encoding="utf-8") as file:
        i = 0
        for player in players:
            i += 1
            print(player)
            basic_info = nba_utils.get_basic_info(player.replace("'", "''"))
            best_info = nba_utils.get_best_season(player.replace("'", "''"))
            file.write(f"#### {i}：**{basic_info.get('chinese_name')}**\n\n")
            file.write(
                f"![{basic_info.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{basic_info.get('code')}_{tag}.png)\n\n")
            file.write(
                f"选秀：**{basic_info.get('draft_year')}**年第**{basic_info.get('draft_position')}**顺位,一共效力联盟{best_info.get('total_season')}个赛季\n\n")
            pd_str = ImageUtils().format_draw_data(basic_info.get('code'), tag,
                                                   best_info.get('best_hit_rate').replace("，", " | "),
                                                   best_info.get('best_data'))
            file.write(f"最佳赛季：{best_info.get('best_season')}，效力于{best_info.get('best_team')}\n\n")

            file.write(f"最佳赛季数据：**{pd_str}**\n\n")
            file.write(f"命中率：{best_info.get('best_hit_rate')}\n\n")

            file.write("---\n\n")


def this_season(players, tag):
    datas = []
    for p in players:
        this_season = nba_utils.get_game_log_with_season(p.replace("'", "''"), 2024)
        basic_info = nba_utils.get_basic_info(p.replace("'", "''"))
        basic_info.update(this_season)

        datas.append(basic_info)

    sorted_datas = sorted(datas, key=lambda x: x['this_data'][0], reverse=True)

    file_name = os.path.join(file_path, f"{today}_{tag}.md")
    with open(file_name, "w", encoding="utf-8") as file:
        i = len(sorted_datas)
        for data in reversed(sorted_datas):
            # if data['this_score'] < 10:
            #     continue

            print(data)
            file.write(f"#### {i}：**{data.get('this_team')}-{data.get('chinese_name')}**\n\n")
            if not data.get('draft_position'):
                file.write(f"选秀：**{data.get('draft_year')}**年落选秀\n\n")
            elif data.get('draft_position') == 1:
                file.write(f"选秀：**{data.get('draft_year')}**年状元秀\n\n")
            elif data.get('draft_position') == 2:
                file.write(f"选秀：**{data.get('draft_year')}**年榜眼秀\n\n")
            elif data.get('draft_position') == 3:
                file.write(f"选秀：**{data.get('draft_year')}**年探花秀\n\n")
            else:
                file.write(f"选秀：**{data.get('draft_year')}**年第**{data.get('draft_position')}**顺位\n\n")
            ImageUtils().draw_text(data.get('code'), tag, data.get('this_hit_rate').replace("，", " | "), (
                '┏',
                '得分：', f"{data.get('this_data')[0]}",
                '篮板：', f"{data.get('this_data')[1]}",
                '助攻：', f"{data.get('this_data')[2]}",
                '抢断：', f"{data.get('this_data')[3]}",
                '盖帽：', f"{data.get('this_data')[4]}",
                '┛'))
            file.write(
                f"![{data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{data.get('code')}_{tag}.png)\n\n")
            if not data.get('this_attend'):
                file.write("本赛季尚未获得出场机会\n\n")
            else:
                file.write(
                    f"本赛季已经代表{data.get('this_team')}出战{data.get('this_attend')}场比赛，取得{data.get('this_win')}胜{data.get('this_loss')}负的战绩\n\n")
                file.write(
                    f"本赛季数据：**{data.get('this_data')[0]}分 | {data.get('this_data')[1]}篮板 | {data.get('this_data')[2]}助攻 | {data.get('this_data')[3]}抢断 | {data.get('this_data')[4]}盖帽**\n\n")
                file.write(f"命中率：{data.get('this_hit_rate')}\n\n")
                # file.write(
                #     f"投篮：{data.get('this_fg')[0]}/{data.get('this_fg')[1]}，三分球：**{data.get('this_fg3')[0]}**/{data.get('this_fg3')[1]}，罚球：{data.get('this_ft')[0]}/{data.get('this_ft')[1]}\n\n")
                # file.write(f"上赛季数据：**{data.get('last_data')}**\n\n")
                file.write("---\n\n")
            i -= 1


def improvement_player(players):
    improvement_players = []
    for player in players:
        last_season = nba_utils.get_player_last_season_data(player.replace("'", "''"))
        if not last_season.get('last_score') or last_season.get('last_score') < 12:
            continue
        this_season = nba_utils.get_game_log_with_season(player.replace("'", "''"), 2024)
        if this_season.get('this_attend') < 5:
            continue
        if this_season.get('this_score') - last_season.get('last_score') < -8:
            basic_info = nba_utils.get_basic_info(player.replace("'", "''"))
            basic_info.update(last_season)
            basic_info.update(this_season)
            improvement_players.append(basic_info)
    for info in improvement_players:
        print(info)

    sorted_datas = sorted(improvement_players, key=lambda x: x['this_data'][0], reverse=True)
    tag = 'descend'
    file_name = os.path.join(file_path, f"{today}_{tag}.md")
    with open(file_name, "w", encoding="utf-8") as file:
        i = len(sorted_datas)
        for data in reversed(sorted_datas):
            print(data)
            file.write(f"#### {i}：**{data.get('this_team')}-{data.get('chinese_name')}**\n\n")
            if not data.get('draft_position'):
                file.write(f"选秀：**{data.get('draft_year')}**年落选秀\n\n")
            elif data.get('draft_position') == 1:
                file.write(f"选秀：**{data.get('draft_year')}**年状元秀\n\n")
            elif data.get('draft_position') == 2:
                file.write(f"选秀：**{data.get('draft_year')}**年榜眼秀\n\n")
            elif data.get('draft_position') == 3:
                file.write(f"选秀：**{data.get('draft_year')}**年探花秀\n\n")
            else:
                file.write(f"选秀：**{data.get('draft_year')}**年第**{data.get('draft_position')}**顺位\n\n")
            ImageUtils().draw_text(data.get('code'), tag, data.get('this_hit_rate').replace("，", " | "), (
                '┏',
                '得分：', f"{data.get('this_data')[0]}",
                '篮板：', f"{data.get('this_data')[1]}",
                '助攻：', f"{data.get('this_data')[2]}",
                '抢断：', f"{data.get('this_data')[3]}",
                '盖帽：', f"{data.get('this_data')[4]}",
                '┛'))
            file.write(
                f"![{data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{data.get('code')}_{tag}.png)\n\n")
            file.write(
                f"上赛季数据：**{data.get('last_data')}**\n\n")
            file.write(
                f"本赛季已经代表{data.get('this_team')}出战{data.get('this_attend')}场比赛，取得**{data.get('this_win')}胜{data.get('this_loss')}负**的战绩\n\n")
            file.write(
                f"本赛季数据：**{data.get('this_data')[0]}分 | {data.get('this_data')[1]}篮板 | {data.get('this_data')[2]}助攻 | {data.get('this_data')[3]}抢断 | {data.get('this_data')[4]}盖帽**\n\n")
            file.write(f"命中率：{data.get('this_hit_rate')}\n\n")

            # file.write(
            #     f"投篮：{data.get('this_fg')[0]}/{data.get('this_fg')[1]}，三分球：{data.get('this_fg3')[0]}/{data.get('this_fg3')[1]}，罚球：{data.get('this_ft')[0]}/{data.get('this_ft')[1]}\n\n")
            # file.write(f"上赛季数据：**{data.get('last_data')}**\n\n")
            file.write("---\n\n")
            i -= 1

    print(improvement_players)


def season_data(players, tag):
    player_datas = []
    for player in players:
        player_name = player.get('player_name').replace("'", "''")
        season = player.get('draft_year') + 2
        season_data = nba_utils.get_game_log_with_season(player_name, season)
        basic_info = nba_utils.get_basic_info(player_name)
        basic_info.update(season_data)
        player_datas.append(basic_info)

    sorted_datas = sorted(player_datas, key=lambda x: x['this_data'][0])
    file_name = os.path.join(file_path, f"{today}_{tag}.md")
    with open(file_name, "w", encoding="utf-8") as file:
        i = len(sorted_datas)
        for data in sorted_datas:
            print(data)
            file.write(f"#### {i}：**{data.get('this_team')}-{data.get('chinese_name')}**\n\n")

            if not data.get('draft_position'):
                file.write(f"选秀：**{data.get('draft_year')}**年落选秀\n\n")
            elif data.get('draft_position') == 1:
                file.write(f"选秀：**{data.get('draft_year')}**年状元秀\n\n")
            elif data.get('draft_position') == 2:
                file.write(f"选秀：**{data.get('draft_year')}**年榜眼秀\n\n")
            elif data.get('draft_position') == 3:
                file.write(f"选秀：**{data.get('draft_year')}**年探花秀\n\n")
            else:
                file.write(f"选秀：**{data.get('draft_year')}**年第**{data.get('draft_position')}**顺位\n\n")
            ImageUtils().draw_text(data.get('code'), tag, data.get('this_hit_rate').replace("，", " | "), (
                '┏',
                '得分：', f"{data.get('this_data')[0]}",
                '篮板：', f"{data.get('this_data')[1]}",
                '助攻：', f"{data.get('this_data')[2]}",
                '抢断：', f"{data.get('this_data')[3]}",
                '盖帽：', f"{data.get('this_data')[4]}",
                '┛'))
            file.write(
                f"![{data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{data.get('code')}_{tag}.png)\n\n")
            if not data.get('this_attend'):
                file.write("未参加任何比赛\n\n")
            else:
                file.write(
                    f"代表{data.get('this_team')}出战{data.get('this_attend')}场比赛，取得**{data.get('this_win')}胜{data.get('this_loss')}负**的战绩\n\n")
                file.write(
                    f"赛季数据：**{data.get('this_data')[0]}分 | {data.get('this_data')[1]}篮板 | {data.get('this_data')[2]}助攻 | {data.get('this_data')[3]}抢断 | {data.get('this_data')[4]}盖帽**\n\n")
                file.write(f"命中率：{data.get('this_hit_rate')}\n\n")
            i -= 1


if __name__ == '__main__':
    usa_players = ['Paolo Banchero', 'Austin Reaves', 'Josh Hart', 'Cameron Johnson', 'Walker Kessler', 'Mikal Bridges',
                   'Anthony Edwards', 'Tyrese Haliburton', 'Brandon Ingram', 'Jaren Jackson Jr.', 'Bobby Portis',
                   'Jalen Brunson']
    # 选秀年过滤
    # player_list = get_sql(
    #     "select * from public.player_draft where draft_position =3 and draft_year>2000 and draft_year <2023 order by draft_year;")
    # season_data(player_list, 3)

    # 现役球员
    # player_list = get_sql("select player_name from public.player_active;")
    # players = [player.get('player_name') for player in player_list]
    # improvement_player(players)
    # sql = f"""SELECT player_name FROM public.player_regular_gamelog WHERE season=2024 GROUP BY player_name HAVING SUM(fg3) >= 15 and (SUM(fg3) / SUM(fg3a::float)) >= 0.4 ;"""
    # player_list = get_sql(sql)
    # for p in player_list:
    #     print(p)
    # players = [player.get('player_name') for player in player_list]
    # this_season(players, '3pt')
    sql = """SELECT prg.*
FROM public.player_draft prg
INNER JOIN public.player_active pa
ON prg.player_name = pa.player_name
WHERE  prg.team = 'HOU' order by prg.draft_year;
"""
    player_list = get_sql(sql)
    players = [player.get('player_name') for player in player_list]
    players.extend(['Kenyon Martin Jr.', 'Alperen Sengun', 'TyTy Washington Jr.'])
    this_season(players, 'hou')
