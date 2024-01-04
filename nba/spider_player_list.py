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

big_contract = [
    {
        'player_name': 'Jakob Poeltl',
        'contract': "4年8000万美金",
        'name': '雅各布·珀尔特尔',
        'team': "猛龙",
        'activity': False,
    },
    {
        'player_name': 'Josh Hart',
        'contract': "4年8100万美金",
        'name': '约什·哈特',
        'team': "尼克斯",
        'activity': False,
    },
    {
        'player_name': 'Dillon Brooks',
        'contract': "4年8600万美金",
        'name': '狄龙·布鲁克斯',
        'team': "火箭",
        'activity': False,
    },
    {
        'player_name': 'Draymond Green',
        'contract': "4年1亿美金",
        'name': '德雷蒙德·格林',
        'team': "勇士",
        'activity': False,
    },
    {
        'player_name': 'Kyle Kuzma',
        'contract': "4年1.02亿美金",
        'name': '凯尔·库兹马',
        'team': "奇才",
        'activity': False,
    },
    {
        'player_name': 'Khris Middleton',
        'contract': "3年1.02亿美金",
        'name': '克里斯·米德尔顿',
        'team': "雄鹿",
        'activity': False,
    },
    {
        'player_name': 'Cameron Johnson',
        'contract': "4年1.08亿美金",
        'name': '卡梅伦·约翰逊',
        'team': "篮网",
        'activity': False,
    },
    {
        'player_name': 'Dejounte Murray',
        'contract': "4年1.2亿美金",
        'name': '德章泰·默里',
        'team': "老鹰",
        'activity': False,
    },
    {
        'player_name': 'Kyrie Irving',
        'contract': "3年1.26亿美金",
        'name': '凯里·欧文',
        'team': "独行侠",
        'activity': False,
    },
    {
        'player_name': 'Fred VanVleet',
        'contract': "3年1.3亿美金",
        'name': '弗雷德·范弗利特',
        'team': "火箭",
        'activity': False,
    },
    {
        'player_name': 'Jaden McDaniels',
        'contract': "5年1.36亿美金",
        'name': '杰登·麦克丹尼尔斯',
        'team': "森林狼",
        'activity': False,
    },
    {
        'player_name': 'Devin Vassell',
        'contract': "5年1.46亿美金",
        'name': '德文·瓦塞尔',
        'team': "马刺",
        'activity': False,
    },
    {
        'player_name': 'Jerami Grant',
        'contract': "5年1.6亿美金",
        'name': '杰拉米·格兰特',
        'team': "开拓者",
        'activity': False,
    },
    {
        'player_name': 'Giannis Antetokounmpo',
        'contract': "3年1.86亿美金",
        'name': '扬尼斯·阿德托昆博',
        'team': "雄鹿",
        'activity': False,
    },
    {
        'player_name': 'Anthony Davis',
        'contract': "3年1.86亿美金",
        'name': '安东尼·戴维斯',
        'team': "湖人",
        'activity': False,
    },
    {
        'player_name': 'Desmond Bane',
        'contract': "5年2.07亿美金",
        'name': '戴斯蒙德·贝恩',
        'team': "雄鹿",
        'activity': False,
    },
    {
        'player_name': 'Domantas Sabonis',
        'contract': "5年2.17亿美金",
        'name': '多曼塔斯·萨博尼斯',
        'team': "国王",
        'activity': False,
    },
    {
        'player_name': 'Tyrese Haliburton',
        'contract': "5年2.6亿美金",
        'name': '泰瑞斯·哈利伯顿',
        'team': "步行者",
        'activity': False,
    },
    {
        'player_name': 'LaMelo Ball',
        'contract': "5年2.6亿美金",
        'name': '拉梅洛·鲍尔',
        'team': "黄蜂",
        'activity': False,
    },
    {
        'player_name': 'Anthony Edwards',
        'contract': "5年2.6亿美金",
        'name': '安东尼·爱德华兹',
        'team': "森林狼",
        'activity': False,
    },
    {
        'player_name': 'Jaylen Brown',
        'contract': "5年3.04亿美金",
        'name': '杰伦·布朗',
        'team': "凯尔特人",
        'activity': False,
    },
]

stars = [
    "LeBron James", "Joel Embiid", "Kyrie Irving", "Luka Doncic", "Nikola Jokic", "Anthony Edwards", "Jaylen Brown",
    "Paul George", "Tyrese Haliburton", "Julius Randle", "De'Aaron Fox", "Jaren Jackson Jr.", "Giannis Antetokounmpo",
    "Jayson Tatum", "Ja Morant", "Donovan Mitchell", "Lauri Markkanen", "Damian Lillard", "Jrue Holiday",
    "Shai Gilgeous-Alexander", "DeMar DeRozan", "Pascal Siakam", "Bam Adebayo", "Domantas Sabonis", "Kevin Durant",
    "Stephen Curry", "Zion Williamson"
]
new_star = ['Tyrese Maxey', 'Desmond Bane', 'Jalen Brunson', 'Kyle Kuzma', 'Jerami Grant', 'Mikal Bridges',
            'Dejounte Murray', 'Cade Cunningham', 'RJ Barrett', 'Alperen Sengun', 'Paolo Banchero', 'Jalen Green',
            'Franz Wagner', 'Victor Wembanyama', 'Evan Mobley', 'Scottie Barnes', 'Chet Holmgren']

img_util = ImageUtils()


def best_season(players, tag):
    file_name = os.path.join(file_path, f"{today}_{tag}")
    with open(file_name, "w", encoding="utf-8") as file:
        i = 0
        for player_info in players:
            i += 1
            print(player_info)
            player = player_info.get('player_name')
            basic_info = nba_utils.get_basic_info(player.replace("'", "''"))
            best_info = nba_utils.get_best_season(player.replace("'", "''"))
            career = nba_utils.career_data(player.replace("'", "''"))
            file.write(f"#### {i}、**{basic_info.get('chinese_name')}**\n\n")
            file.write(
                f"![{basic_info.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{basic_info.get('code')}_{best_info.get('best_team')}_{tag}_{i}.png)\n\n")
            file.write(
                f"选秀：**{basic_info.get('draft_year')}**年第**{basic_info.get('draft_position')}**顺位（**{nba_teams.get(basic_info.get('draft_team'))}选中**）\n\n")
            img_data = ['┏', f"{best_info.get('best_data')[0]} 分",
                        f"{best_info.get('best_data')[1]} 篮板",
                        f"{best_info.get('best_data')[2]} 助攻",
                        f"{best_info.get('best_data')[3]} 抢断",
                        f"{best_info.get('best_data')[4]} 盖帽",
                        f"{best_info.get('best_data')[5]} 失误", "┛"]
            hit_rate = f"投篮：{round(best_info.get('best_hit_rate')[0] * 100 / best_info.get('best_hit_rate')[1], 1)}% | 三分：{round(best_info.get('best_hit_rate')[2] * 100 / best_info.get('best_hit_rate')[3], 1)}% | 罚球：{round(best_info.get('best_hit_rate')[4] * 100 / best_info.get('best_hit_rate')[5], 1)}%"
            img_util.draw_text(basic_info.get('code'), best_info.get('best_team'), tag,
                               hit_rate,
                               img_data, i)
            teams = career.get('teams_played_for')
            team = '、'.join((set(nba_teams.get(item) for item in teams)))
            file.write(
                f"职业生涯一共出战{career.get('total_games')}场比赛，效力过{team}，场均贡献 **{round(career.get('data')[0] / career.get('total_games'), 1)}分{round(career.get('data')[1] / career.get('total_games'), 1)}篮板{round(career.get('data')[2] / career.get('total_games'), 1)}助攻{round(career.get('data')[3] / career.get('total_games'), 1)}抢断{round(career.get('data')[4] / career.get('total_games'), 1)}盖帽**\n\n")

            file.write(f"最佳赛季：{best_info.get('best_season')}，效力于{nba_teams.get(best_info.get('best_team'))}\n\n")

            file.write(
                f"赛季数据：**{best_info.get('best_data')[0]}分 | {best_info.get('best_data')[1]}篮板 | {best_info.get('best_data')[2]}助攻 | {best_info.get('best_data')[3]}抢断 | {best_info.get('best_data')[4]}盖帽 **\n\n")
            file.write(f"{hit_rate}\n\n")

            file.write("---\n\n\n")


def week_best(players):
    datas = []
    tag = 'weekly'
    for player in players:
        player_name = player.get('player_name').replace("'", "''")
        last_week = nba_utils.last_week_data(player_name)
        if last_week.get('game_win') < 2:
            continue
        if last_week.get('game_score') / last_week.get('game_attend') <= 30:
            continue
        if last_week.get('game_win') <= last_week.get('game_loss'):
            continue
        this_season = nba_utils.get_game_log_with_season(player_name, 2024)
        basic_info = nba_utils.get_basic_info(player_name)
        basic_info.update(last_week)
        basic_info.update(this_season)
        print(basic_info)

        datas.append(basic_info)

    sorted_datas = sorted(datas, key=lambda x: x['game_score'] / x['game_attend'], reverse=True)

    file_name = os.path.join(file_path, f"{today}_{tag}.md")
    with open(file_name, "w", encoding="utf-8") as file:
        i = 1
        for data in reversed(sorted_datas[:10]):

            print(data)
            file.write(f"#### {i}、 **{data.get('chinese_name')}-{nba_teams.get(data.get('this_team'))}**\n\n")
            # for item in big_contract:
            #     if item['player_name'] == data.get("player_name"):
            #         contract = item['contract']
            #         file.write(f"薪金：**{contract}**\n\n")

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

            img_data = ['┏', f"{data.get('game_data')[0]} 分",
                        f"{data.get('game_data')[1]} 篮板",
                        f"{data.get('game_data')[2]} 助攻",
                        f"{data.get('game_data')[3]} 抢断",
                        f"{data.get('game_data')[4]} 盖帽",
                        f"{data.get('game_data')[5]} 失误", "┛"]
            hit_rate = f"投篮：{round(int(data.get('game_hit_rate')[0] * 100 / data.get('game_hit_rate')[1]))}% | 三分：{round(int(data.get('game_hit_rate')[2] * 100 / data.get('game_hit_rate')[3]))}% | 罚球：{round(int(data.get('game_hit_rate')[4] * 100 / data.get('game_hit_rate')[5]))}%"
            img_util.draw_text(data.get('code'), data.get('this_team'), tag, hit_rate, img_data, i)
            file.write(
                f"![{data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{data.get('code')}_{data.get('this_team')}_{tag}_{i}.png)\n\n")
            if not data.get('game_attend'):
                file.write("上周未出战任何比赛\n\n")
            else:
                win_opp = "、".join([nba_teams.get(item) for item in data.get('win_opp')])
                loss_opp = "、".join([nba_teams.get(item) for item in data.get('loss_opp')])
                if not win_opp:
                    if data.get('game_loss') == 1:
                        file.write(
                            f"上周出战1场比赛，上场{data.get('game_time')}，**不敌{loss_opp}**\n\n")
                    else:
                        file.write(
                            f"上周出战{data.get('game_attend')}场比赛，场均上场{data.get('game_time')}，**{data.get('game_loss')}战全败({loss_opp})**\n\n")
                elif not loss_opp:
                    if data.get('game_win') == 1:
                        file.write(
                            f"上周出战1场比赛，上场{data.get('game_time')}，**战胜{win_opp}**\n\n")
                    else:
                        file.write(
                            f"上周出战{data.get('game_attend')}场比赛，场均上场{data.get('game_time')}，**{data.get('game_win')}战全胜（{win_opp}）**\n\n")
                else:
                    file.write(
                        f"上周出战{data.get('game_attend')}场比赛，场均上场{data.get('game_time')}，**{data.get('game_win')}胜({win_opp}){data.get('game_loss')}负({loss_opp})**\n\n")
                file.write(
                    f"数据：**{data.get('game_data')[0]}分 | {data.get('game_data')[1]}篮板 | {data.get('game_data')[2]}助攻 | {data.get('game_data')[3]}抢断 | {data.get('game_data')[4]}盖帽 | {data.get('game_data')[5]}失误**\n\n")

                file.write(
                    f"{hit_rate}\n\n")
                # file.write(
                #     f"投篮：{data.get('this_fg')[0]}/{data.get('this_fg')[1]}，三分球：**{data.get('this_fg3')[0]}**/{data.get('this_fg3')[1]}，罚球：{data.get('this_ft')[0]}/{data.get('this_ft')[1]}\n\n")
                file.write("---\n\n\n")
            i += 1


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
            'opp': res.get('opp'),
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
            file.write(f"#### {i}、**{basic_info.get('chinese_name')}**\n\n")
            file.write(f"职业生涯{len(datas)}次解锁这一成就\n\n")
            file.write(
                f"![{basic_info.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{basic_info.get('code')}_{basic_info.get('team')}_{tag}_0.png)\n\n")
            for data in datas:
                if data.get('pts') > max_score:
                    max_score = data.get('pts')
                    max_record = data

                file.write(
                    f"- 在{data.get('game_date')}，{nba_teams.get(data.get('team'))}对阵{nba_teams.get(data.get('opp'))}的比赛中，得到**{data.get('pts')}分 | {data.get('reb')}篮板 | {data.get('ast')}助攻 | {data.get('stl')}抢断 | {data.get('blk')}盖帽**\n\n")
            high_scores[basic_info.get('code')] = max_record
            file.write("---\n\n\n")
            i += 1
        for key, data in high_scores.items():
            print(key, data)
            img_util.draw_text(key, data.get('team'), tag, data.get('hit_rate').replace("，", " | "), (
                '┏',
                f"{data.get('pts')} 分",
                f"{data.get('reb')} 篮板",
                f"{data.get('ast')} 助攻",
                f"{data.get('stl')} 抢断",
                f"{data.get('blk')} 盖帽",
                '┛'), 0)


def latest_games(players, num, tag):
    datas = []
    for p in players:
        p = p.get('player_name')
        sql = f"""SELECT id, player_name, season, game_date, up, playing_time, pts, reb, oreb, dreb, ast, fga, fg, fg3a, fg3, fta, ft, stl, blk, tov, plus_minus, team, opp, game_win FROM public.player_regular_gamelog where player_name ='{p.replace("'", "''")}' and up=True and season=2024 and game_date >= '2023-11-30';
                                """
        print(p)
        latest_data = nba_utils.get_game_data(sql)
        this_season = nba_utils.get_game_log_with_season(p.replace("'", "''"), 2024)
        if latest_data.get('game_data')[0] < 25 or latest_data.get('game_attend') < 5:
            continue

        basic_info = nba_utils.get_basic_info(p.replace("'", "''"))
        basic_info.update(latest_data)
        basic_info.update(this_season)
        datas.append(basic_info)

    sorted_datas = sorted(datas, key=lambda x: x['game_data'][0], reverse=True)

    file_name = os.path.join(file_path, f"{today}_{tag}.md")
    with open(file_name, "w", encoding="utf-8") as file:
        i = 10
        for data in reversed(sorted_datas[:10]):
            print(data)
            file.write(f"#### {i}、 **{data.get('chinese_name')}({nba_teams.get(data.get('this_team'))})**\n\n")
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

            img_data = ['┏', f"{data.get('game_data')[0]} 分", f"{data.get('game_data')[1]} 篮板",
                        f"{data.get('game_data')[2]} 助攻", f"{data.get('game_data')[3]} 抢断",
                        f"{data.get('game_data')[4]} 盖帽", f"{data.get('game_data')[5]} 失误", "┛"]
            img_util.draw_text(data.get('code'), data.get('this_team'), tag,
                               data.get('game_hit_rate').replace("，", " | "), img_data, i)
            file.write(
                f"![{data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{data.get('code')}_{data.get('this_team')}_{tag}_{i}.png)\n\n")
            # file.write(
            #     f"本赛季数据：**{data.get('this_data')[0]}分 | {data.get('this_data')[1]}篮板 | {data.get('this_data')[2]}助攻 | {data.get('this_data')[3]}抢断 | {data.get('this_data')[4]}盖帽 | {data.get('this_data')[5]}失误**\n\n")

            file.write(
                f"战绩：**{data.get('game_win')}胜{data.get('game_loss')}负**，场均上场{data.get('game_time')}\n\n")
            file.write(
                f"本月数据：**{data.get('game_data')[0]}分 | {data.get('game_data')[1]}篮板 | {data.get('game_data')[2]}助攻 | {data.get('game_data')[3]}抢断 | {data.get('game_data')[4]}盖帽 | {data.get('game_data')[5]}失误**\n\n")
            file.write(f"本月命中率：{data.get('game_hit_rate')}\n\n")
            file.write("---\n\n\n")
            i -= 1


def this_season(players, tag):
    datas = []
    for player in players:
        player_name = player.replace("'", "''")
        this_season = nba_utils.get_game_log_with_season(player_name, 2024)
        print(this_season)
        # if this_season.get('this_score') < 22:
        #     continue
        # if this_season.get('this_attend') < 10:
        #     continue
        last_season = nba_utils.get_player_last_season_data(player_name)
        # if this_season['this_score'] <= 10 or this_season['this_attend'] < 10:
        #     continue
        basic_info = nba_utils.get_basic_info(player_name)
        basic_info.update(this_season)
        best_game = nba_utils.best_game(player_name, 2024)
        basic_info.update(best_game)
        basic_info.update(last_season)

        datas.append(basic_info)

    sorted_datas = sorted(datas, key=lambda x: x['this_score'], reverse=True)

    file_name = os.path.join(file_path, f"{today}_{tag}.md")
    with open(file_name, "w", encoding="utf-8") as file:
        i = 1
        for data in reversed(sorted_datas):

            print(data)
            file.write(f"#### {i}、 **{data.get('chinese_name')}-{nba_teams.get(data.get('this_team'))}**\n\n")

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
            birth_date = datetime.strptime(str(data.get('birthday')), "%Y-%m-%d")
            current_date = datetime.now()
            file.write(
                f"出生日期：{data.get('birthday')}({int((current_date - birth_date).days / 365)}岁)\n\n")
            # file.write(f"薪金：{nba_utils.get_salary(data.get('player_name'))}\n\n")

            img_data = ['┏', f"{data.get('this_data')[0]} 分", f"{data.get('this_data')[1]} 篮板",
                        f"{data.get('this_data')[2]} 助攻", f"{data.get('this_data')[3]} 抢断",
                        f"{data.get('this_data')[4]} 盖帽", f"{data.get('this_data')[5]} 失误", "┛"]
            hit_rate = f"投篮：{round(int(data.get('this_hit_rate')[0] * 100 / data.get('this_hit_rate')[1]))}% | 三分：{round(int(data.get('this_hit_rate')[2] * 100 / data.get('this_hit_rate')[3]))}% | 罚球：{round(int(data.get('this_hit_rate')[4] * 100 / data.get('this_hit_rate')[5]))}%"
            img_util.draw_text(data.get('code'), data.get('this_team'), tag, hit_rate, img_data, i)
            file.write(
                f"![{data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{data.get('code')}_{data.get('this_team')}_{tag}_{i}.png)\n\n")
            file.write(
                f"上赛季数据：**{data.get('last_data')[0]}分 | {data.get('last_data')[1]}篮板 | {data.get('last_data')[2]}助攻 | {data.get('last_data')[3]}抢断 | {data.get('last_data')[4]}盖帽**\n\n")
            if not data.get('this_attend'):
                file.write("本赛季尚未获得出场机会\n\n")
            else:
                file.write(f"战绩：**{data.get('this_win')}胜{data.get('this_loss')}负**\n\n")
                # file.write(
                #     f"本赛季已出战{data.get('this_attend')}场比赛，场均上场{data.get('this_time')}，取得{data.get('this_win')}胜{data.get('this_loss')}负的战绩\n\n")

                file.write(
                    f"数据：**{data.get('this_data')[0]}分 | {data.get('this_data')[1]}篮板 | {data.get('this_data')[2]}助攻 | {data.get('this_data')[3]}抢断 | {data.get('this_data')[4]}盖帽 | {data.get('this_data')[5]}失误**\n\n")
                win = '战胜' if data.get('game_win') else '不敌'
                file.write(
                    f"{hit_rate}\n\n")
                file.write(
                    f"赛季高光表现：在{data.get('game_date')}{win}{nba_teams.get(data.get('opp'))}的比赛中，上场{str(data.get('playing_time'))[2:]}，**贡献{data.get('pts')}分{data.get('reb')}篮板{data.get('ast')}助攻{data.get('stl')}抢断{data.get('blk')}盖帽**\n\n")
                # if nba_utils.get_honor(data.get('player_name')):
                #     file.write(f"荣誉：{nba_utils.get_honor(data.get('player_name'))}\n\n")
                # file.write(
                #     f"投篮：{data.get('this_fg')[0]}/{data.get('this_fg')[1]}，三分球：**{data.get('this_fg3')[0]}**/{data.get('this_fg3')[1]}，罚球：{data.get('this_ft')[0]}/{data.get('this_ft')[1]}\n\n")
            file.write("---\n\n\n")
            i += 1


def improvement_player(players):
    improvement_players = []
    for player in players:
        player = player.get('player_name')
        last_season = nba_utils.get_player_last_season_data(player.replace("'", "''"))
        if not last_season.get('last_score'):
            continue
        this_season = nba_utils.get_game_log_with_season(player.replace("'", "''"), 2024)
        if this_season.get('this_attend') < 15:
            continue

        basic_info = nba_utils.get_basic_info(player.replace("'", "''"))
        print(basic_info)
        basic_info.update(last_season)
        basic_info.update(this_season)
        improvement_players.append(basic_info)
    for info in improvement_players:
        print(info)

    sorted_datas = sorted(improvement_players,
                          key=lambda x: x.get('this_score') - x.get('last_score'))
    tag = 'improve'
    file_name = os.path.join(file_path, f"{today}_{tag}.md")
    with open(file_name, "w", encoding="utf-8") as file:
        i = len(sorted_datas)
        for data in reversed(sorted_datas):
            print(data)
            file.write(f"#### {i}、**{nba_teams.get(data.get('this_team'))}-{data.get('chinese_name')}**\n\n")
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
            img_util.draw_text(data.get('code'), data.get('this_team'), tag,
                               data.get('this_hit_rate').replace("，", " | "), (
                                   '┏',
                                   f"{data.get('this_data')[0]} 分",
                                   f"{data.get('this_data')[1]} 篮板",
                                   f"{data.get('this_data')[2]} 助攻",
                                   f"{data.get('this_data')[3]} 抢断",
                                   f"{data.get('this_data')[4]} 盖帽",
                                   '┛'), i)
            # file.write(
            #     f"三分下滑：**{round(data.get('this_fg3')[0] * 100 / data.get('this_fg3')[1] - data.get('last_hit_rate')[2] * 100 / data.get('last_hit_rate')[3], 1)}%**\n\n")
            file.write(
                f"![{data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{data.get('code')}_{data.get('this_team')}_{tag}_{i}.png)\n\n")
            file.write(
                f"上赛季数据：**{data.get('last_data')[0]}分 | {data.get('last_data')[1]}篮板 | {data.get('last_data')[2]}助攻 | {data.get('last_data')[3]}抢断 | {data.get('last_data')[4]}盖帽**\n\n")
            file.write(
                f"上赛季命中率：投篮{round(data.get('last_hit_rate')[0] * 100 / data.get('last_hit_rate')[1], 1)}%，**三分{round(data.get('last_hit_rate')[2] * 100 / data.get('last_hit_rate')[3], 1)}%**，罚球{round(data.get('last_hit_rate')[4] * 100 / data.get('last_hit_rate')[5], 1)}%\n\n")
            # file.write(
            #     f"本赛季已经代表{nba_teams.get(data.get('this_team'))}出战{data.get('this_attend')}场比赛，取得**{data.get('this_win')}胜{data.get('this_loss')}负**的战绩\n\n")
            file.write(
                f"本赛季数据：**{data.get('this_data')[0]}分 | {data.get('this_data')[1]}篮板 | {data.get('this_data')[2]}助攻 | {data.get('this_data')[3]}抢断 | {data.get('this_data')[4]}盖帽**\n\n")
            file.write(f"本赛季命中率：{data.get('this_hit_rate')}\n\n")

            # file.write(
            #     f"投篮：{data.get('this_fg')[0]}/{data.get('this_fg')[1]}，三分球：{data.get('this_fg3')[0]}/{data.get('this_fg3')[1]}，罚球：{data.get('this_ft')[0]}/{data.get('this_ft')[1]}\n\n")
            # file.write(f"上赛季数据：**{data.get('last_data')}**\n\n")
            file.write("---\n\n\n")
            i -= 1

    print(improvement_players)


def game_records(players):
    tag = 'record'
    player_datas = []
    for player in players:
        player_name = player.get('player_name').replace("'", "''")
        best_game = get_sql(f"select * from public.player_regular_gamelog where pts>40 and fg3a=0;")
        if not best_game:
            continue
        if best_game[0].get("pts") < 20:
            continue
        basic_info = nba_utils.get_basic_info(player_name)
        this_season = nba_utils.get_game_log_with_season(player_name, 2024)
        best_game.update(this_season)
        best_game.update(basic_info)
        player_datas.append(best_game[0])
        print(best_game)

    sorted_datas = sorted(player_datas, key=lambda x: x['pts'])
    file_name = os.path.join(file_path, f"{today}_{tag}.md")
    with open(file_name, "w", encoding="utf-8") as file:
        i = len(sorted_datas)
        for data in reversed(sorted_datas[:10]):
            print(data)
            file.write(f"#### {i}、**{data.get('chinese_name')}({nba_teams.get(data.get('this_team'))})**\n\n")

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

            hit_rate = f"投篮：{data.get('fg', 0)}/{data.get('fga', 0)} | 三分：{data.get('fg3', 0)}/{data.get('fg3a', 0)} | 罚球：{data.get('ft', 0)}/{data.get('fta', 0)}"
            img_util.draw_text(data.get('code'), data.get('this_team'), tag,
                               hit_rate, ('┏',
                                          f"{data.get('pts', 0)} 分",
                                          f"{data.get('reb', 0)} 篮板",
                                          f"{data.get('ast', 0)} 助攻",
                                          f"{data.get('stl', 0)} 抢断",
                                          f"{data.get('blk', 0)} 盖帽",
                                          f"{data.get('tov', 0)} 失误",
                                          '┛'), i)

            win = '战胜' if data.get('game_win') else '不敌'
            file.write(
                f"![{data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{data.get('code')}_{data.get('this_team')}_{tag}_{i}.png)\n\n")

            file.write(
                f"在{data.get('game_date')}{win}{nba_teams.get(data.get('opp'))}的比赛中，上场{str(data.get('playing_time'))[2:]}，贡献{data.get('pts')}分{data.get('reb')}篮板{data.get('ast')}助攻{data.get('stl')}抢断{data.get('blk')}盖帽\n\n")
            file.write("---\n\n\n")
            i -= 1


def player_compare(players):
    tag = 'compare'
    datas = []
    for player in players:
        player_name = player.get('player_name').replace("'", "''")
        sql = f"select * from public.player_regular_gamelog where player_name='{player_name}' and up=TRUE and game_date>='2023-11-30';"
        game_data = nba_utils.get_game_data(sql)
        if game_data.get('game_score') < 10:
            continue
        basic_info = nba_utils.get_basic_info(player_name)
        basic_info.update(game_data)
        datas.append(basic_info)

    sorted_datas = sorted(datas, key=lambda x: x['game_score'], reverse=True)
    file_name = os.path.join(file_path, f"{today}_{tag}.md")
    with open(file_name, "w", encoding="utf-8") as file:
        i = 1
        for data in sorted_datas[:20]:
            print(data)
            file.write(f"#### {i}、**{data.get('chinese_name')}**\n\n")

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

            hit_rate = f"投篮：{data.get('game_fg')[0]}/{data.get('game_fg')[1]} | 三分：{data.get('game_fg3')[0]}/{data.get('game_fg3')[1]} | 罚球：{data.get('game_ft')[0]}/{data.get('game_ft')[1]}"
            img_util.draw_text(data.get('code'), data.get('game_team'), tag,
                               data.get('game_hit_rate').replace("，", " | "), ('┏',
                                                                               f"{data.get('game_data')[0]} 分",
                                                                               f"{data.get('game_data')[1]} 篮板",
                                                                               f"{data.get('game_data')[2]} 助攻",
                                                                               f"{data.get('game_data')[3]} 抢断",
                                                                               f"{data.get('game_data')[4]} 盖帽",
                                                                               f"{data.get('game_data')[5]} 失误",
                                                                               '┛'), i)
            file.write(
                f"![{data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{data.get('code')}_{data.get('game_team')}_{tag}_{i}.png)\n\n")
            file.write(f"上场时间：{data.get('game_time')}({data.get('game_win')}胜{data.get('game_loss')}负)\n\n")
            file.write(
                f"数据：{data.get('game_data')[0]}分 | {data.get('game_data')[1]}篮板 | {data.get('game_data')[2]}助攻 | {data.get('game_data')[3]}抢断 | {data.get('game_data')[4]}盖帽 | {data.get('game_data')[5]}失误\n\n")
            file.write(f"{data.get('game_hit_rate')}\n\n")
            best_game = nba_utils.best_game(data.get('player_name').replace("'", "''"))
            win = '战胜' if best_game.get('game_win') else '不敌'
            file.write(
                f"最佳表现：在{best_game.get('game_date')}{win}{nba_teams.get(best_game.get('opp'))}的比赛中，上场{str(best_game.get('playing_time'))[2:]}，**贡献{best_game.get('pts')}分{best_game.get('reb')}篮板{best_game.get('ast')}助攻{best_game.get('stl')}抢断{best_game.get('blk')}盖帽**\n\n")

            file.write("---\n\n\n")
            i += 1


def best_game(players, tag):
    player_datas = []
    for player in players:
        player_name = player.get('player_name').replace("'", "''")
        best_game = nba_utils.best_game(player_name)
        if not best_game:
            continue
        basic_info = nba_utils.get_basic_info(player_name)
        this_season = nba_utils.get_game_log_with_season(player_name, 2024)
        best_game.update(this_season)
        best_game.update(basic_info)
        player_datas.append(best_game)
        print(best_game)

    sorted_datas = sorted(player_datas, key=lambda x: x['pts'])
    file_name = os.path.join(file_path, f"{today}_{tag}.md")
    with open(file_name, "w", encoding="utf-8") as file:
        i = 1
        for data in reversed(sorted_datas):
            print(data)
            file.write(f"#### {i}、**{data.get('chinese_name')}({nba_teams.get(data.get('this_team'))})**\n\n")

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

            hit_rate = f"投篮：{data.get('fg', 0)}/{data.get('fga', 0)} | 三分：{data.get('fg3', 0)}/{data.get('fg3a', 0)} | 罚球：{data.get('ft', 0)}/{data.get('fta', 0)}"
            img_util.draw_text(data.get('code'), data.get('this_team'), tag,
                               hit_rate, ('┏',
                                          f"{data.get('pts', 0)} 分",
                                          f"{data.get('reb', 0)} 篮板",
                                          f"{data.get('ast', 0)} 助攻",
                                          f"{data.get('stl', 0)} 抢断",
                                          f"{data.get('blk', 0)} 盖帽",
                                          f"{data.get('tov', 0)} 失误",
                                          '┛'), i)
            if not data.get('this_attend', 0):
                file.write(
                    f"![{data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{data.get('code')}_{data.get('this_team')}_{tag}_{i}.png)\n\n")
                file.write(f"本赛季未出战任何比赛\n\n")
            else:
                win = '战胜' if data.get('game_win') else '不敌'
                file.write(
                    f"![{data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{data.get('code')}_{data.get('this_team')}_{tag}_{i}.png)\n\n")
                file.write(
                    f"本赛季已出战{data.get('this_attend')}场比赛，场均上场{data.get('this_time')}，{data.get('this_win')}胜{data.get('this_loss')}负\n\n")
                if data.get('plus_minus') > 0:
                    file.write(
                        f"赛季最佳表现：在{data.get('game_date')}{win}{nba_teams.get(data.get('opp'))}的比赛中，上场{str(data.get('playing_time'))[2:]}，贡献{data.get('pts')}分{data.get('reb')}篮板{data.get('ast')}助攻，正负值为+{data.get('plus_minus')}\n\n")
                else:
                    file.write(
                        f"赛季最佳表现：在{data.get('game_date')}{win}{nba_teams.get(data.get('opp'))}的比赛中，上场{str(data.get('playing_time'))[2:]}，贡献{data.get('pts')}分{data.get('reb')}篮板{data.get('ast')}助攻，正负值为{data.get('plus_minus')}\n\n")
                file.write(
                    f"本赛季：**{data.get('this_data')[0]}分 | {data.get('this_data')[1]}篮板 | {data.get('this_data')[2]}助攻 | {data.get('this_data')[3]}抢断 | {data.get('this_data')[4]}盖帽 | {data.get('this_data')[5]}失误**\n\n")
                file.write(
                    f"投篮：{round(data.get('this_hit_rate')[0] * 100 / data.get('this_hit_rate')[1], 1)}% | 三分：{round(data.get('this_hit_rate')[2] * 100 / data.get('this_hit_rate')[3], 1)}% | 罚球：{round(data.get('this_hit_rate')[4] * 100 / data.get('this_hit_rate')[5], 1)}%\n\n")

            file.write("---\n\n\n")
            i += 1


def career_data(players, tag):
    player_datas = []
    for player in players:
        player_name = player.get('player_name').replace("'", "''")
        career = nba_utils.career_data(player_name)
        if career.get('total_games') <= 200:
            continue
        basic_info = nba_utils.get_basic_info(player_name)
        this_season = nba_utils.get_game_log_with_season(player_name, 2024)
        career.update(basic_info)
        career.update(this_season)
        player_datas.append(career)

    sorted_datas = sorted(player_datas, key=lambda x: x['data'][0] / x['total_games'], reverse=True)
    file_name = os.path.join(file_path, f"{today}_{tag}.md")
    with open(file_name, "w", encoding="utf-8") as file:
        i = 20
        for data in reversed(sorted_datas[:20]):
            print(data)
            file.write(f"#### 第{i}顺位、**{data.get('chinese_name')}**\n\n")

            if not data.get('draft_position'):
                file.write(f"原选秀：**{data.get('draft_year')}**年落选秀\n\n")
            elif data.get('draft_position') == 1:
                file.write(f"原选秀：**{data.get('draft_year')}**年状元秀\n\n")
            elif data.get('draft_position') == 2:
                file.write(f"原选秀：**{data.get('draft_year')}**年榜眼秀\n\n")
            elif data.get('draft_position') == 3:
                file.write(f"原选秀：**{data.get('draft_year')}**年探花秀\n\n")
            else:
                file.write(
                    f"原选秀：**{data.get('draft_year')}**年第**{data.get('draft_position')}**顺位\n\n")
            teams = data.get('teams_played_for')
            team = '、'.join((set(nba_teams.get(item) for item in teams)))
            # file.write(
            #     f"累计出战{data.get('total_games')}场比赛（{data['total_win']}胜{data['total_loss']}负），**胜率：{round(data['total_win'] * 100 / data['total_games'], 1)}%**\n\n")
            # file.write(f"进球总数：**{int(data.get('total_fg'))}**，三分进球数：**{data.get('total_fg3')}**\n\n")
            # file.write(f"总得分：**{data.get('total_points')}**")
            # file.write(
            #     f"球队：生涯共效力过**{team}**{len(set(teams))}支球队，累计出战**{data.get('total_games')}**场比赛,得到**{data.get('total_points')}**分\n\n")
            hit_rate = f"投篮：{round(int(data.get('hit_rate')[0]) * 100 / int(data.get('hit_rate')[1]), 1)}% | 三分：{round(int(data.get('hit_rate')[2]) * 100 / int(data.get('hit_rate')[3]), 1)}% | 罚球：{round(int(data.get('hit_rate')[4]) * 100 / int(data.get('hit_rate')[5]), 1)}%"
            img_util.draw_text(data.get('code'), data.get('this_team'), tag,
                               hit_rate, ('┏',
                                          f"{round(data.get('data')[0] / data.get('total_games'), 1)} 分",
                                          f"{round(data.get('data')[1] / data.get('total_games'), 1)} 篮板",
                                          f"{round(data.get('data')[2] / data.get('total_games'), 1)} 助攻",
                                          f"{round(data.get('data')[3] / data.get('total_games'), 1)} 抢断",
                                          f"{round(data.get('data')[4] / data.get('total_games'), 1)} 盖帽",
                                          f"{round(data.get('data')[5] / data.get('total_games'), 1)} 失误",
                                          '┛'), i)
            file.write(
                f"![{data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{data.get('code')}_{data.get('this_team')}_{tag}_{i}.png)\n\n")
            # file.write(
            #     f"本赛季：**{data.get('this_data')[0]}分 | {data.get('this_data')[1]}篮板 | {data.get('this_data')[2]}助攻 | {data.get('this_data')[3]}抢断 | {data.get('this_data')[4]}盖帽 | {data.get('this_data')[5]}失误**\n\n")
            #
            file.write(
                f"生涯数据：**{round(data.get('data')[0] / data.get('total_games'), 1)}分 | {round(data.get('data')[1] / data.get('total_games'), 1)}篮板 | {round(data.get('data')[2] / data.get('total_games'), 1)}助攻 | {round(data.get('data')[3] / data.get('total_games'), 1)}抢断 | {round(data.get('data')[4] / data.get('total_games'), 1)}盖帽 | {round(data.get('data')[5] / data.get('total_games'), 1)}失误**\n\n")
            file.write(f"{hit_rate}\n\n")
            file.write(
                f"胜率：{data.get('total_games')}场比赛（{data['total_win']}胜{data['total_loss']}负），**{round(data['total_win'] * 100 / data['total_games'], 1)}%**\n\n")
            honors = nba_utils.get_honor(data.get('player_name').replace("'", "''"))
            if honors:
                file.write(f"荣誉：{honors}\n\n")
            file.write("---\n\n\n")

            i -= 1


def season_data(players, tag):
    player_datas = []
    for player in players:
        player_name = player.get('player_name').replace("'", "''")
        season = player.get('draft_year') + 2
        season_data = nba_utils.get_game_log_with_season(player_name, season)

        basic_info = nba_utils.get_basic_info(player_name)
        basic_info.update(season_data)
        print(basic_info)
        player_datas.append(basic_info)

    sorted_datas = sorted(player_datas, key=lambda x: x['this_score'])
    file_name = os.path.join(file_path, f"{today}_{tag}.md")
    with open(file_name, "w", encoding="utf-8") as file:
        i = len(sorted_datas)
        for data in sorted_datas:
            print(data)
            retirement = '现役'
            if data.get('retirement') != 2023:
                retirement = f"{data.get('retirement')}年退役"
            file.write(f"#### {i}、 **{data.get('chinese_name')}**\n\n")

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
            img_util.draw_text(data.get('code'), data.get('this_team'), tag,
                               data.get('this_hit_rate').replace("，", " | "), (
                                   '┏',
                                   f"{data.get('this_data')[0]} 分",
                                   f"{data.get('this_data')[1]} 篮板",
                                   f"{data.get('this_data')[2]} 助攻",
                                   f"{data.get('this_data')[3]} 抢断",
                                   f"{data.get('this_data')[4]} 盖帽",
                                   '┛'), i)
            file.write(
                f"![{data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{data.get('code')}_{data.get('this_team')}_{tag}_{i}.png)\n\n")
            if not data.get('this_attend'):
                file.write("未参加任何比赛\n\n")
            else:
                file.write(
                    f"{data.get('draft_year') + 3}赛季代表{nba_teams.get(data.get('this_team'))}出战{data.get('this_attend')}场比赛，取得**{data.get('this_win')}胜{data.get('this_loss')}负**的战绩\n\n")
                file.write(
                    f"赛季数据：**{data.get('this_data')[0]}分 | {data.get('this_data')[1]}篮板 | {data.get('this_data')[2]}助攻 | {data.get('this_data')[3]}抢断 | {data.get('this_data')[4]}盖帽**\n\n")
                file.write(f"命中率：{data.get('this_hit_rate')}\n\n")
            file.write("---\n\n\n")
            i -= 1


def fail(players):
    datas = []
    tag = 'fail'
    for player in players:
        player_name = player.get('player_name')
        fail_res = get_sql(f"""WITH PlayerResults AS (
              SELECT
                player_name,
                game_date,
                game_win,
                up,
                season,
                ROW_NUMBER() OVER (PARTITION BY player_name, season ORDER BY game_date) -
                ROW_NUMBER() OVER (PARTITION BY player_name, season, game_win ORDER BY game_date) AS grp
              FROM
                public.game_result_view
              WHERE
                player_name = '{player_name}'
                AND up = TRUE
            )
            , LongestLosingStreak AS (
              SELECT
                player_name,
                season,
                MIN(game_date) AS start_date,
                MAX(game_date) AS end_date,
                COUNT(*) AS streak_length
              FROM
                PlayerResults
              WHERE
                game_win = FALSE
              GROUP BY
                player_name,
                season,
                grp
            )
            SELECT
              player_name,
              season,
              start_date,
              end_date,
              streak_length
            FROM
              LongestLosingStreak
            ORDER BY
              streak_length DESC
            LIMIT 1;
            """)
        season = fail_res[0].get('season')
        season_data = nba_utils.get_game_log_with_season(player_name, season)
        basic_info = nba_utils.get_basic_info(player_name)
        basic_info.update(season_data)
        basic_info.update(fail_res[0])

        datas.append(basic_info)
    sorted_datas = sorted(datas, key=lambda x: x['streak_length'])
    file_name = os.path.join(file_path, f"{today}_{tag}.md")
    with open(file_name, "w", encoding="utf-8") as file:
        i = 1
        for data in sorted_datas:
            print(data)
            file.write(f"#### {i}、 **{data.get('chinese_name')}**\n\n")
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
            hit_rate = f"投篮：{round(int(data.get('this_hit_rate')[0]) * 100 / int(data.get('this_hit_rate')[1]), 1)}% | 三分：{round(int(data.get('this_hit_rate')[2]) * 100 / int(data.get('this_hit_rate')[3]), 1)}% | 罚球：{round(int(data.get('this_hit_rate')[4]) * 100 / int(data.get('this_hit_rate')[5]), 1)}%"
            img_util.draw_text(data.get('code'), data.get('this_team'), tag,
                               hit_rate, (
                                   '┏',
                                   f"{data.get('this_data')[0]} 分",
                                   f"{data.get('this_data')[1]} 篮板",
                                   f"{data.get('this_data')[2]} 助攻",
                                   f"{data.get('this_data')[3]} 抢断",
                                   f"{data.get('this_data')[4]} 盖帽",
                                   '┛'), i)
            file.write(
                f"![{data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{data.get('code')}_{data.get('this_team')}_{tag}_{i}.png)\n\n")
            file.write(
                f"最长连败：**{data.get('streak_length')}连败**，发生在{data.get('season')}赛季，{data.get('start_date')}到{data.get('end_date')}期间\n\n")
            # file.write(
            #     f"该赛季代表{nba_teams.get(data.get('this_team'))}出战{data.get('this_attend')}场比赛，取得**{data.get('this_win')}胜{data.get('this_loss')}负**的战绩\n\n")
            file.write(
                f"赛季数据：**{data.get('this_data')[0]}分 | {data.get('this_data')[1]}篮板 | {data.get('this_data')[2]}助攻 | {data.get('this_data')[3]}抢断 | {data.get('this_data')[4]}盖帽**\n\n")
            file.write(f"{hit_rate}\n\n")
            file.write("---\n\n\n")
            i += 1


def top_game(sql, tag):
    top_games = get_sql(sql)
    file_name = os.path.join(file_path, f"{today}_{tag}.md")
    players = []
    datas = {}
    texts = []
    with open(file_name, "w", encoding="utf-8") as file:
        i = 1
        for game in top_games:
            player_name = game.get('player_name').replace("'", "''")
            basic_info = nba_utils.get_basic_info(player_name)
            this_season = nba_utils.get_game_log_with_season(player_name, 2024)
            basic_info.update(this_season)
            basic_info.update(game)
            print(basic_info)
            file.write(f"#### {i}、**{basic_info.get('chinese_name')}({nba_teams.get(basic_info.get('team'))})**\n\n")

            if not basic_info.get('draft_position'):
                file.write(f"选秀：**{basic_info.get('draft_year')}**年落选秀\n\n")
            elif basic_info.get('draft_position') == 1:
                file.write(f"选秀：**{basic_info.get('draft_year')}**年状元秀\n\n")
            elif basic_info.get('draft_position') == 2:
                file.write(f"选秀：**{basic_info.get('draft_year')}**年榜眼秀\n\n")
            elif basic_info.get('draft_position') == 3:
                file.write(f"选秀：**{basic_info.get('draft_year')}**年探花秀\n\n")
            else:
                file.write(
                    f"选秀：**{basic_info.get('draft_year')}**年第**{basic_info.get('draft_position')}**顺位\n\n")

            hit_rate = f"投篮：{basic_info.get('fg', 0)}/{basic_info.get('fga', 0)} | 三分：{basic_info.get('fg3', 0)}/{basic_info.get('fg3a', 0)} | 罚球：{basic_info.get('ft', 0)}/{basic_info.get('fta', 0)}"
            img_util.draw_text(basic_info.get('code'), basic_info.get('team'), tag,
                               hit_rate, ('┏',
                                          f"{basic_info.get('pts', 0)} 分",
                                          f"{basic_info.get('reb', 0)} 篮板",
                                          f"{basic_info.get('ast', 0)} 助攻",
                                          f"{basic_info.get('stl', 0)} 抢断",
                                          f"{basic_info.get('blk', 0)} 盖帽",
                                          f"{basic_info.get('tov', 0)} 失误",
                                          '┛'), i)

            win = '战胜' if basic_info.get('game_win') else '不敌'
            file.write(
                f"![{basic_info.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{basic_info.get('code')}_{basic_info.get('team')}_{tag}_{i}.png)\n\n")

            file.write(
                f"{basic_info.get('game_date')}，在{nba_teams.get(basic_info.get('team'))}{win}{nba_teams.get(basic_info.get('opp'))}的比赛中，上场{str(basic_info.get('playing_time'))[2:]}，贡献**{basic_info.get('pts')}分{basic_info.get('reb')}篮板{basic_info.get('ast')}助攻{basic_info.get('stl')}抢断{basic_info.get('blk')}盖帽{basic_info.get('tov')}失误**\n\n")
            file.write("---\n\n\n")
            stress = f"{basic_info.get('pts')}分{basic_info.get('reb')}篮板"
            if basic_info.get('ast'):
                stress += f"{basic_info.get('ast')}助攻"
            if basic_info.get('stl'):
                stress += f"{basic_info.get('stl')}抢断"
            if basic_info.get('blk'):
                stress += f"{basic_info.get('blk')}盖帽"
            players.append({
                "player_name": f"{player_name.replace(' ', '_')}-{basic_info.get('game_date')}",
                "chinese_name": basic_info.get('chinese_name'),
                "stress": stress,
                "extra": [f"{basic_info.get('game_date')},{nba_teams.get(basic_info.get('team'))}Vs{nba_teams.get(basic_info.get('opp'))}",
                          hit_rate.replace(" | ", " ")
                          ]
            })

            txt = f"第{i}名，{basic_info.get('chinese_name')}，{basic_info.get('game_date')}，在{nba_teams.get(basic_info.get('team'))}{win}{nba_teams.get(basic_info.get('opp'))}的比赛中，全场贡献{basic_info.get('pts')}分{basic_info.get('reb')}篮板"
            if basic_info.get('ast'):
                txt += f"{basic_info.get('ast')}助攻"
            if basic_info.get('stl'):
                txt += f"{basic_info.get('stl')}抢断"
            if basic_info.get('blk'):
                txt += f"{basic_info.get('blk')}盖帽"

            texts.append(txt)

            i += 1
    print(";".join(texts))
    img_util.long_img(players, "high")


if __name__ == '__main__':
    usa_players = ['Paolo Banchero', 'Austin Reaves', 'Josh Hart', 'Cameron Johnson', 'Walker Kessler', 'Mikal Bridges',
                   'Anthony Edwards', 'Tyrese Haliburton', 'Brandon Ingram', 'Jaren Jackson Jr.', 'Bobby Portis',
                   'Jalen Brunson']
    old_rockets = [
        'TyTy Washington Jr.',
        'Daishen Nix',
        'Josh Christopher',
        'Usman Garuba',
        'Kenyon Martin Jr.',

    ]
    rocket_2018 = ['Chris Paul',
                   'James Harden',
                   'P.J. Tucker',
                   'Eric Gordon',
                   'Clint Capela',
                   'Isaiah Hartenstein',
                   ]
    rookies = ['Victor Wembanyama', 'Chet Holmgren', 'Ausar Thompson', 'Jordan Hawkins', 'Dereck Lively II',
               'Brandon Miller', 'Jaime Jaquez Jr.', 'Keyonte George', 'Bilal Coulibaly', 'Marcus Sasser']

    # player_list = ['Jalen Green', 'Tari Eason', 'Jabari Smith Jr.']
    # player_compare(player_list)
    # players = []
    # names = ['Thompson', 'Holiday', 'Lopez', 'Curry', 'Murray', 'Anteto', 'Morris', 'Mobley', 'Bridges','Ball']
    # for name in names:
    #     players.extend(get_sql(f"select * from public.player_active where player_name like '%{name}%' order by birthday;"))
    # # players = get_sql("select * from public.player_active where player_name like '%Jackson%' order by birthday;")
    # this_season(players, 'bro')

    # sql = "select * from public.player_active;"
    # players = get_sql(sql)
    # latest_games(players, 1, 12)

    c = ['Chet Holmgren', 'Victor Wembanyama', 'Alperen Sengun', 'James Harden', 'Zion Williamson', 'Kyrie Irving',
         'Paul George', 'Anthony Davis', 'Domantas Sabonis',
         'Jaren Jackson Jr.', 'Karl-Anthony Towns', "De'Aaron Fox", 'Kawhi Leonard', 'Shai Gilgeous-Alexander', 'Anthony Edwards',
         'Nikola Jokic', 'Kevin Durant', 'Luka Doncic', 'Stephen Curry', 'LeBron James', ]
    # this_season(rocket_2018, '2018')
    sql = "SELECT * FROM public.player_regular_gamelog WHERE (pts+reb+ast+stl+blk)>=70 and game_date between '2023-01-01' and '2023-12-31' order by pts desc,reb desc limit 20;"
    top_game(sql, 'top')
    # players=['Jalen Green','Jordan Poole','Jordan Clarkson','Coby White']
    # sql = "select * from public.player_active where draft_year=2017;"
    # players = get_sql(sql)
    # player_compare(players)

    # sql = "select * from public.player_honors where honor='2021-22 最佳新秀阵容';"
    # players = get_sql(sql)
    # this_season(old_rockets, 'navie')
    # sql = "select * FROM public.player_active;"
    # improvement_player(get_sql(sql))
