# -*- coding: utf-8 -*-
from datetime import datetime, date

import requests

from nba.constants import nba_teams
from nba.sqlUtils import store_to_db, get_sql


def get_all_active_players():
    url = 'https://china.nba.cn/stats2/league/playerlist.json?locale=zh_CN'

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': 'privacyV2=true; AMCV_248F210755B762187F000101%40AdobeOrg=-1712354808%7CMCIDTS%7C19648%7CMCMID%7C48517773620589826003359889172843151504%7CMCAAMLH-1698118772%7C11%7CMCAAMB-1698118772%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1697521172s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.3.0; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218b370b56581cf-00a9790305208498-26031151-2073600-18b370b565964f%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThiMzcwYjU2NTgxY2YtMDBhOTc5MDMwNTIwODQ5OC0yNjAzMTE1MS0yMDczNjAwLTE4YjM3MGI1NjU5NjRmIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218b370b56581cf-00a9790305208498-26031151-2073600-18b370b565964f%22%7D; _ga=GA1.2.902210438.1697680174; _ga_H1HTS9RJXW=GS1.2.1697680174.1.1.1697680248.0.0.0; i18next=zh_CN; locale=zh_CN; countryCode=CN; acw_tc=0b328f1a16981272244611154ec52560db329bec73851c849cb91d82e4caee',
        'If-None-Match': '"428432-a66cfe46d52802fd95eb569d45737dcd36ea7767"',
        'Referer': 'https://china.nba.cn/players/vs/',
        'Sec-Fetch-Dest': 'empty',
        'Cache-Control': 'no-cache',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.get(url, headers=headers)

    # 打印响应内容
    result = response.json()
    players = []
    for player in result.get("payload", {}).get('players'):
        players.append((
            player.get("playerProfile").get("playerId"),
            player.get("playerProfile").get("code"),
            player.get("playerProfile").get("displayNameEn"),
            player.get("playerProfile").get("displayName").replace(" ", "·"),
            int(player.get("playerProfile").get("draftYear")),
            player.get("teamProfile").get("name"),
            player.get("teamProfile").get("nameEn"),
            player.get("playerProfile").get("height"),
            player.get("playerProfile").get("weight"),
            player.get("playerProfile").get("position"),
        ))

    sql = f"""INSERT INTO public.player_active (player_id, code, player_name, chinese_name, draft_year,  team, team_en, height, body_weight, "position")
                VALUES(%s, %s, %s, %s,%s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
            """
    store_to_db(sql, players)
    return players


if __name__ == '__main__':
    sql = """select code,player_name,chinese_name,draft_year,team,draft_position from public.player_active where draft_year<2023 and draft_position >0"""
    players = get_sql(sql)
    # get_all_active_players()
    sorted_players = sorted(players, key=lambda x: x['draft_year'], reverse=True)
    num_count = {}
    for player in sorted_players:
        if player.get("draft_year") not in num_count.keys():
            num_count[player.get("draft_year")] = [player]
        else:
            player_list = num_count.get(player.get("draft_year"))
            if player.get("draft_position") != 0:
                player_list.append(player)
                num_count[player.get("draft_year")] = player_list

    today = datetime.now().strftime("%Y-%m-%d")
    file_name = f"F:\\notebooks\\其他\\draft\\{today}_num.md"
    with open(file_name, "w", encoding="utf-8") as file:
        i = 0
        for item in num_count.items():
            active_players = sorted(item[1], key=lambda x: x['draft_position'])
            i += 1
            file.write(f"#### {i}. {item[0]}年\n")
            first_player = active_players[0]
            last_player = active_players[-1]
            file.write(
                f"&emsp;&emsp;目前还有{len(item[1])}名球员在联盟效力，其中选秀顺位最高的是**第{first_player.get('draft_position')}顺位的{first_player.get('chinese_name')}**，选秀顺位最低的是**第{last_player.get('draft_position')}顺位的{last_player.get('chinese_name')}**\n\n")
            print(item[0], len(item[1]), sorted(item[1], key=lambda x: x['draft_position']))
            file.write("---\n\n")
            file.write(f"**第{first_player.get('draft_position')}顺位-{first_player.get('chinese_name')}**\n\n")

            sql = f"""SELECT player_name,team,game_attend, minutes_attend, pts, reb,  ast, fga, fg, fg3a, fg3, fta, ft, stl, blk, tov, salary
                        FROM public.player_regular_total_season where player_name='{first_player.get('player_name')}' and season='2022-23';
                    """
            first_data = get_sql(sql)
            print(first_data)
            if not len(first_data):
                file.write(f"上赛季未出战任何比赛\n\n")
                continue
            first_attend = first_data[0].get('game_attend')
            file.write(f"上赛季效力于{nba_teams.get(first_data[0].get('team'))}，共出战{first_attend}场比赛\n\n")
            # file.write(f"薪水：{int(first_data[0].get('salary') / 1000)}万")
            file.write(
                f"场均贡献：**{round(first_data[0].get('pts') / first_attend, 1)}分 | {round(first_data[0].get('reb') / first_attend, 1)}篮板 | {round(first_data[0].get('ast') / first_attend, 1)}助攻 | {round(first_data[0].get('stl') / first_attend, 1)}抢断 | {round(first_data[0].get('blk') / first_attend, 1)}盖帽**\n\n")
            file.write(
                f"命中率：投篮{round(first_data[0].get('fg') / first_data[0].get('fga') * 100, 1)}%，三分球{round(first_data[0].get('fg3') / first_data[0].get('fg3a') * 100, 1)}%，罚球{round(first_data[0].get('ft') / first_data[0].get('fta') * 100, 1)}%\n\n")
            file.write(
                f"![{first_player.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\img\\{first_player.get('code')}.png)\n\n")

            file.write("---\n\n")
            file.write(f"**第{last_player.get('draft_position')}顺位-{last_player.get('chinese_name')}**\n\n")
            sql = f"""SELECT player_name,team,game_attend, minutes_attend, pts, reb,  ast, fga, fg, fg3a, fg3, fta, ft, stl, blk, tov,salary
                                    FROM public.player_regular_total_season where player_name='{last_player.get('player_name')}'and season='2022-23';
                                """
            last_data = get_sql(sql)
            print(last_data)
            if not len(last_data):
                file.write(f"上赛季未出战任何比赛\n\n")
                continue
            last_attend = first_data[0].get('game_attend')
            file.write(f"上赛季效力于{nba_teams.get(last_data[0].get('team'))}，共出战{last_attend}场比赛\n\n")
            # file.write(f"薪水：{int(last_data[0].get('salary') / 1000)}万")
            file.write(
                f"场均贡献**{round(last_data[0].get('pts') / last_attend, 1)}分 | {round(last_data[0].get('reb') / last_attend, 1)}篮板 | {round(last_data[0].get('ast') / last_attend, 1)}助攻 | {round(last_data[0].get('stl') / last_attend, 1)}抢断 | {round(last_data[0].get('blk') / last_attend, 1)}盖帽**\n\n")
            file.write(
                f"命中率：投篮{round(last_data[0].get('fg') / last_data[0].get('fga') * 100, 1)}%，三分球{round(last_data[0].get('fg3') / last_data[0].get('fg3a') * 100, 1)}%，罚球{round(last_data[0].get('ft') / last_data[0].get('fta') * 100, 1)}%\n\n")
            file.write(
                f"![{last_player.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\img\\{last_player.get('code')}.png)\n\n")
