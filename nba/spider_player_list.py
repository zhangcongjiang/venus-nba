# -*- coding: utf-8 -*-
import os
from datetime import datetime

from nba.constants import nba_teams
from tools.image_utils import ImageUtils
from tools.nba_utils import NbaUtils
from tools.sqlUtils import get_sql

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
            pd_str = ImageUtils().format_draw_data(basic_info.get('code'), basic_info.get('best_ream'), tag,
                                                   best_info.get('best_hit_rate').replace("，", " | "),
                                                   best_info.get('best_data'))
            file.write(f"最佳赛季：{best_info.get('best_season')}，效力于{best_info.get('best_team')}\n\n")

            file.write(f"最佳赛季数据：**{pd_str}**\n\n")
            file.write(f"命中率：{best_info.get('best_hit_rate')}\n\n")

            file.write("---\n\n")


def game_data(sql, tag):
    players = {}
    result = get_sql(sql)

    for res in result:
        if res.get("player_name") not in players.keys():
            players[res.get('player_name')] = []
        hit_rate = ''
        if res.get('fga'):
            hit_rate += f"投篮{round(res.get('fg') / res.get('fga') * 100, 1)}%，"
        if res.get('fg3a'):
            hit_rate += f"三分{round(res.get('fg3') / res.get('fg3a') * 100, 1)}%，"
        if res.get('fta'):
            hit_rate += f"罚球{round(res.get('ft') / res.get('fta') * 100, 1)}%"
        values = {
            'game_date': res.get('game_date'),
            'pts': res.get('pts'),
            'reb': res.get('reb'),
            'ast': res.get('ast'),
            'stl': res.get('stl'),
            'blk': res.get('blk'),
            'team': res.get('team'),
            'opp': nba_teams.get(res.get('opp')),
            'hit_rate': hit_rate
        }
        datas = players.get(res.get('player_name'))
        datas.append(values)
        players[res.get('player_name')] = datas

    sorted_dict = dict(sorted(players.items(), key=lambda item: len(item[1])))
    file_name = os.path.join(file_path, f"{today}_{tag}")
    with open(file_name, "w", encoding="utf-8") as file:
        i = 1
        high_scores = {}
        for player, datas in sorted_dict.items():
            print(player, datas)
            max_record = {}
            max_score = 0
            basic_info = nba_utils.get_basic_info(player.replace("'", "''"))
            file.write(f"#### {i}：**{basic_info.get('chinese_name')}**\n\n")
            file.write(f"职业生涯{len(datas)}次空砍50+\n\n")
            file.write(
                f"![{basic_info.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{basic_info.get('code')}_{tag}.png)\n\n")
            for data in datas:
                if data.get('pts') > max_score:
                    max_score = data.get('pts')
                    max_record = data

                file.write(
                    f"- 在{data.get('game_date')}，{data.get('team')}不敌{data.get('opp')}的比赛中，空砍**{data.get('pts')}分 | {data.get('reb')}篮板 | {data.get('ast')}助攻 | {data.get('stl')}抢断 | {data.get('blk')}盖帽**\n\n")
            high_scores[basic_info.get('code')] = max_record

            i += 1
        for key, data in high_scores.items():
            print(key, data)
            ImageUtils().draw_text(key, data.get('team'), tag, data.get('hit_rate').replace("，", " | "), (
                '┏',
                '得分：', f"{data.get('pts')}",
                '篮板：', f"{data.get('reb')}",
                '助攻：', f"{data.get('ast')}",
                '抢断：', f"{data.get('stl')}",
                '盖帽：', f"{data.get('blk')}",
                '┛'))


def this_season(players, tag):
    datas = []
    for p in players:
        this_season = nba_utils.get_game_log_with_season(p.replace("'", "''"), 2024)
        print(this_season)
        if this_season['this_data'][0] < 5:
            continue
        basic_info = nba_utils.get_basic_info(p.replace("'", "''"))
        basic_info.update(this_season)

        datas.append(basic_info)

    sorted_datas = sorted(datas, key=lambda x: x['this_score'])

    file_name = os.path.join(file_path, f"{today}_{tag}.md")
    with open(file_name, "w", encoding="utf-8") as file:
        i = len(sorted_datas)
        for data in sorted_datas:

            print(data)
            file.write(f"#### {i}：**{data.get('chinese_name')}**\n\n")
            if not data.get('draft_position'):
                file.write(f"选秀顺位：**{data.get('draft_year')}**年落选秀\n\n")
            elif data.get('draft_position') == 1:
                file.write(f"选秀顺位：**{data.get('draft_year')}**年状元秀\n\n")
            elif data.get('draft_position') == 2:
                file.write(f"选秀顺位：**{data.get('draft_year')}**年榜眼秀\n\n")
            elif data.get('draft_position') == 3:
                file.write(f"选秀顺位：**{data.get('draft_year')}**年探花秀\n\n")
            else:
                file.write(f"选秀顺位：**{data.get('draft_year')}**年第**{data.get('draft_position')}**顺位\n\n")
            img_data = ['┏', '得分：', f"{data.get('this_data')[0]}", '篮板：', f"{data.get('this_data')[1]}", '助攻：',
                        f"{data.get('this_data')[2]}"]
            if data.get('this_data')[3] >= 0.5:
                img_data.extend(['抢断：', f"{data.get('this_data')[3]}"])
            if data.get('this_data')[4] >= 0.5:
                img_data.extend(['盖帽：', f"{data.get('this_data')[4]}"])
            if data.get('this_data')[5] >= 0.5:
                img_data.extend(['失误：', f"{data.get('this_data')[5]}"])
            img_data.append('┛')
            ImageUtils().draw_text(data.get('code'), data.get('this_team'), tag,
                                   data.get('this_hit_rate').replace("，", " | "), img_data, i)
            file.write(
                f"![{data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{data.get('code')}_{tag}_{i}.png)\n\n")
            if not data.get('this_attend'):
                file.write("本赛季尚未获得出场机会\n\n")
            else:
                file.write(f"**重排顺位：第{i}顺位**\n\n")
                file.write(
                    f"当前效力于{nba_teams.get(data.get('this_team'))}，本赛季已经出战{data.get('this_attend')}场比赛，取得{data.get('this_win')}胜{data.get('this_loss')}负的战绩\n\n")
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
            ImageUtils().draw_text(data.get('code'), data.get('this_team'), tag,
                                   data.get('this_hit_rate').replace("，", " | "), (
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


def career_data(players, tag):
    player_datas = []
    for player in players:
        player_name = player.get('player_name').replace("'", "''")
        career = nba_utils.career_data(player_name)

        basic_info = nba_utils.get_basic_info(player_name)
        career.update(basic_info)
        player_datas.append(career)

    sorted_datas = sorted(player_datas, key=lambda x: x['total_rebounds'], reverse=True)
    file_name = os.path.join(file_path, f"{today}_{tag}.md")
    with open(file_name, "w", encoding="utf-8") as file:
        i = 20
        for data in reversed(sorted_datas[:20]):
            print(data)
            file.write(f"#### {i}：**{data.get('chinese_name')}**\n\n")

            if not data.get('draft_position'):
                file.write(f"选秀：**{data.get('draft_year')}**年落选秀\n\n")
            elif data.get('draft_position') == 1:
                file.write(f"选秀：**{data.get('draft_year')}**年状元秀\n\n")
            elif data.get('draft_position') == 2:
                file.write(f"选秀：**{data.get('draft_year')}**年榜眼秀\n\n")
            elif data.get('draft_position') == 3:
                file.write(f"选秀：**{data.get('draft_year')}**年探花秀\n\n")
            else:
                file.write(
                    f"选秀：**{data.get('draft_year')}**年第**{data.get('draft_position')}**顺位\n\n")
            teams = data.get('teams_played_for')
            team = '、'.join([nba_teams.get(item) for item in teams])
            file.write(f"总篮板：**{data.get('total_rebounds')}**\n\n")
            file.write(f"球队：生涯共效力过**{team}**{len(teams)}支球队，累计出战**{data.get('total_games')}**场比赛\n\n")
            hit_rate = f"投篮，{data.get('hit_rate')[0]}% | 三分，{data.get('hit_rate')[1]}% | 罚球，{data.get('hit_rate')[2]}%"
            ImageUtils().draw_text(data.get('code'), data.get('teams_played_for')[-1], tag,
                                   hit_rate, (
                                       '┏',
                                       '得分：', f"{data.get('data')[0]}",
                                       '篮板：', f"{data.get('data')[1]}",
                                       '助攻：', f"{data.get('data')[2]}",
                                       '抢断：', f"{data.get('data')[3]}",
                                       '盖帽：', f"{data.get('data')[4]}",
                                       '┛'), i)
            file.write(
                f"![{data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{data.get('code')}_{tag}_{i}.png)\n\n")
            file.write(
                f"生涯数据：**{data.get('data')[0]}分 | {data.get('data')[1]}篮板 | {data.get('data')[2]}助攻 | {data.get('data')[3]}抢断 | {data.get('data')[4]}盖帽**\n\n")
            file.write(f"命中率：{hit_rate}\n\n")
            i -= 1


def season_data(players, tag):
    player_datas = []
    for player in players:
        player_name = player.get('player_name').replace("'", "''")
        season = player.get('draft_year') + 3
        season_data = nba_utils.get_game_log_with_season(player_name, season)
        basic_info = nba_utils.get_basic_info(player_name)
        basic_info.update(season_data)
        print(basic_info)
        player_datas.append(basic_info)

    sorted_datas = sorted(player_datas, key=lambda x: x['this_data'][0])
    file_name = os.path.join(file_path, f"{today}_{tag}.md")
    with open(file_name, "w", encoding="utf-8") as file:
        i = len(sorted_datas)
        for data in sorted_datas:
            print(data)
            retirement = '现役'
            if data.get('retirement') != 2023:
                retirement = f"{data.get('retirement')}年退役"
            file.write(f"#### {i}：**{data.get('chinese_name')}**\n\n")

            if not data.get('draft_position'):
                file.write(f"选秀：**{data.get('draft_year')}**年落选秀({retirement})\n\n")
            elif data.get('draft_position') == 1:
                file.write(f"选秀：**{data.get('draft_year')}**年状元秀({retirement})\n\n")
            elif data.get('draft_position') == 2:
                file.write(f"选秀：**{data.get('draft_year')}**年榜眼秀({retirement})\n\n")
            elif data.get('draft_position') == 3:
                file.write(f"选秀：**{data.get('draft_year')}**年探花秀({retirement})\n\n")
            else:
                file.write(
                    f"选秀：**{data.get('draft_year')}**年第**{data.get('draft_position')}**顺位({retirement})\n\n")
            ImageUtils().draw_text(data.get('code'), data.get('this_team'), tag,
                                   data.get('this_hit_rate').replace("，", " | "), (
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
                    f"{data.get('draft_year') + 3}赛季代表{nba_teams.get(data.get('this_team'))}出战{data.get('this_attend')}场比赛，取得**{data.get('this_win')}胜{data.get('this_loss')}负**的战绩\n\n")
                file.write(
                    f"赛季数据：**{data.get('this_data')[0]}分 | {data.get('this_data')[1]}篮板 | {data.get('this_data')[2]}助攻 | {data.get('this_data')[3]}抢断 | {data.get('this_data')[4]}盖帽**\n\n")
                file.write(f"命中率：{data.get('this_hit_rate')}\n\n")
            i -= 1


if __name__ == '__main__':
    usa_players = ['Paolo Banchero', 'Austin Reaves', 'Josh Hart', 'Cameron Johnson', 'Walker Kessler', 'Mikal Bridges',
                   'Anthony Edwards', 'Tyrese Haliburton', 'Brandon Ingram', 'Jaren Jackson Jr.', 'Bobby Portis',
                   'Jalen Brunson']
    old_rockets = [
        'TyTy Washington Jr.',
        'Daishen Nix',
        'Josh Christopher',
        'Usman Garuba',
        'Kenyon Martin Jr.'
    ]
    rookies = ['Victor Wembanyama', 'Chet Holmgren', 'Ausar Thompson', 'Jordan Hawkins', 'Dereck Lively II',
               'Brandon Miller', 'Jaime Jaquez Jr.', 'Keyonte George', 'Bilal Coulibaly', 'Marcus Sasser']
    # 选秀年过滤
    # player_list = get_sql(
    #     "select * from public.player_draft where draft_position =16 and draft_year>2001 and draft_year <2023 order by draft_year;")
    # season_data(player_list, 17)
    # water_players = get_sql(
    #     "select * from public.player_draft where draft_year =2022  order by draft_year,draft_position;")
    # result = [player.get('player_name') for player in water_players]
    # this_season(result, '2021')
    # 现役球员
    # player_list = get_sql("select player_name from public.player_active;")
    # players = [player.get('player_name') for player in player_list]
    # improvement_player(players)
    # sql = f"""SELECT player_name FROM public.player_draft WHERE draft_year=2019;"""
    # player_list = get_sql(sql)
    # for p in player_list:
    #     print(p)
    # players = [player.get('player_name') for player in player_list]
    # this_season(rookies, 'rookies')
    # sql = """SELECT prg.*
    # FROM public.player_draft prg
    # INNER JOIN public.player_active pa
    # ON prg.player_name = pa.player_name
    # WHERE  prg.team = 'LAL' order by prg.draft_year;
    # """
    # player_list = get_sql(sql)
    # players = [player.get('player_name') for player in player_list]
    #
    # this_season(players, 'lakers')
    # sql = """select * from public.player_regular_gamelog where pts>=50 and game_win =false and season >=2003 order by game_date;"""
    # game_data(sql, 50)
    # sql = """SELECT player_name
    #     FROM public.player_regular_gamelog
    #     WHERE season = 2024 and up=True
    #     GROUP BY player_name
    #     HAVING COUNT(*) = SUM(CASE WHEN game_win = false THEN 1 ELSE 0 END)
    #        AND COUNT(*) > 0;"""
    # player_list = get_sql(sql)
    # players = [player.get('player_name') for player in player_list]
    # this_season(players, 'no_win')

    sql = "select * from public.player_active where draft_year<=2018 and draft_position>0;"
    player_list = get_sql(sql)
    career_data(player_list, 'top20')
