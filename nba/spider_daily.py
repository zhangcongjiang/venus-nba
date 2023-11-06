# -*- coding: utf-8 -*-

import random
import time
import traceback
from datetime import datetime, date

import requests

from nba.sqlUtils import get_sql, store_to_db


def get_player_stats(player):
    url = f"http://china.nba.cn/stats2/player/stats.json?locale=zh_CN&playerCode={player.get('code')}"

    # requests_cache.install_cache('example_cache', expire_after=3600 * 24)
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'acw_tc=0bdd346216970285458832633eae5694b1df7212045652e18fe1d946a4e2ae; i18next=zh_CN; locale=zh_CN; countryCode=CN; sajssdk_2015_cross_new_user=1; privacyV2=true; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218b1ec8a95e80-0d488d073be8ae8-26031e51-1327104-18b1ec8a95f12c5%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThiMWVjOGE5NWU4MC0wZDQ4OGQwNzNiZThhZTgtMjYwMzFlNTEtMTMyNzEwNC0xOGIxZWM4YTk1ZjEyYzUifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218b1ec8a95e80-0d488d073be8ae8-26031e51-1327104-18b1ec8a95f12c5%22%7D',
        'If-None-Match': '"10026-1c17bef8a63b7454a86f96bc0af10df2f5e4d2cf"',
        'Referer': 'http://china.nba.cn/players/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers, verify=False)  # 设置verify=False忽略SSL证书验证

    if response.status_code == 200:
        data = response.json()
        if not data:
            return
        player_datas = {}
        latest_games = data.get('payload', {}).get('player', {}).get('stats', {}).get('seasonGames')
        # print(latest_games)
        last_5_games = data.get('payload', {}).get('player', {}).get('stats', {}).get('playerSplit').get(
            'last5Games').get('statAverage')
        for game in latest_games:
            today = date.today().strftime("%Y-%m-%d")
            # print(f"今天时间：{today}")
            # 中美时间相差12小时
            game_date = int(game.get('profile', {}).get('utcMillis')) + 12 * 60 * 60 * 1000
            formatted_date = datetime.utcfromtimestamp(game_date / 1000).strftime('%Y-%m-%d')
            if formatted_date == today:
                profile = game.get('profile')
                team = profile.get('teamProfile', {}).get('city') + profile.get('teamProfile', {}).get('displayAbbr')
                opp = profile.get('oppTeamProfile', {}).get('city') + profile.get('oppTeamProfile', {}).get(
                    'displayAbbr')

                win_or_loss = profile.get('winOrLoss')
                win = True if win_or_loss == 'won' else False

                stat = game.get('statTotal', {})
                min = int(stat.get('mins'))

                if min > 0:
                    seconds = str(stat.get('secs')).zfill(2)

                    up_time = f"{min} minutes {seconds} seconds"
                    pts = stat.get('points')
                    rebs = int(stat.get('rebs'))
                    asts = int(stat.get('assists'))
                    blks = int(stat.get('blocks'))
                    stls = int(stat.get('steals'))
                    tov = int(stat.get('turnovers'))
                    player_datas['data'] = {
                        '得分：': pts,
                        '篮板：': rebs,
                        '助攻：': asts,
                        '抢断：': stls,
                        '盖帽：': blks,
                        '失误：': tov
                    }
                    print(player.get('id'), player.get('player_name'), player_datas['data'])
                    data = (
                        player.get('player_name'), 2024, today, True, up_time, pts, rebs, 0, 0, asts,
                        int(stat.get('fga')),
                        int(stat.get('fgm')), int(stat.get('tpa')), int(stat.get('tpm')), int(stat.get('fta')),
                        int(stat.get('ftm')), stls, blks, tov, 0, '', '', win)

                    sql = """
                    INSERT INTO public.player_regular_gamelog
                    (player_name, season, game_date, up, playing_time, pts, reb, oreb, dreb, ast, fga, fg, fg3a, fg3, fta, ft, stl, blk, tov, plus_minus, team, opp, game_win)
                    VALUES(%s, %s, %s, %s, %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s);
                    
                    """
                    store_to_db(sql, [data])

    else:
        print('Failed to retrieve data. Status code:', response.status_code)


if __name__ == '__main__':
    sql = """
        SELECT id, player_id, code, player_name, chinese_name, draft_year, draft_position, team, team_en, height, body_weight, "position"
FROM public.player_active where id >0  order by id;
    """

    players = get_sql(sql)
    for player in players:
        try:
            stat = get_player_stats(player)
            random_number = random.randint(2, 4)
            time.sleep(random_number)
        except Exception:
            print(traceback.format_exc())
            print(f"err,{player.get('draft_position')}")
