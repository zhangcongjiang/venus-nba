from datetime import datetime
import random
import sys

import requests
from bs4 import BeautifulSoup
import time


from tools.sqlUtils import store_to_db, get_sql

today = datetime.now().strftime("%Y-%m-%d")


def request_statics(response, name, year):
    # 使用Beautiful Soup解析HTML
    soup = BeautifulSoup(response, 'html.parser')
    # 使用find方法查找具有id="pgl_basic"的表格
    try:
        regular_table = soup.find('table', {'id': 'pgl_basic'})
    except Exception:
        return

    # print(season)
    regular_data = []

    # 检查是否找到表格
    if regular_table:
        tbody = regular_table.find('tbody')
        tr_tags = tbody.find_all('tr')
        for tr in tr_tags:
            if tr.get('class') and 'thead' in tr.get('class'):
                continue
            date_game = tr.find('td', {'data-stat': 'date_game'}).text
            if date_game != today:
                continue

            team = tr.find('td', {'data-stat': 'team_id'}).text
            opp = tr.find('td', {'data-stat': 'opp_id'}).text
            # game_id = tr.find('th', {'data-stat': 'ranker'}).text
            game_result = tr.find('td', {'data-stat': 'game_result'}).text
            game_win = True if game_result.split(" ")[0] == 'W' else False
            if tr.get('id') and tr.get('id').startswith('pgl_basic.'):
                up = True
                playing_time = tr.find('td', {'data-stat': 'mp'}).text
                split_playing_time = playing_time.split(":")
                try:
                    format_playing_time = f"{split_playing_time[0]} minutes {split_playing_time[1]} seconds"
                except Exception:
                    format_playing_time = '0 minutes 0 seconds'
                try:
                    pts = int(tr.find('td', {'data-stat': 'pts'}).text)
                except Exception:
                    pts = 0
                try:
                    oreb = int(tr.find('td', {'data-stat': 'orb'}).text)
                except Exception:
                    oreb = 0
                try:
                    dreb = int(tr.find('td', {'data-stat': 'drb'}).text)
                except Exception:
                    dreb = 0
                try:
                    reb = int(tr.find('td', {'data-stat': 'trb'}).text)
                except Exception:
                    reb = 0
                try:
                    ast = int(tr.find('td', {'data-stat': 'ast'}).text)
                except Exception:
                    ast = 0
                try:
                    fga = int(tr.find('td', {'data-stat': 'fga'}).text)
                except Exception:
                    fga = 0
                try:
                    fg = int(tr.find('td', {'data-stat': 'fg'}).text)
                except Exception:
                    fg = 0
                try:
                    fg3a = int(tr.find('td', {'data-stat': 'fg3a'}).text)
                except Exception:
                    fg3a = 0
                try:
                    fg3 = int(tr.find('td', {'data-stat': 'fg3'}).text)
                except Exception:
                    fg3 = 0
                try:
                    fta = int(tr.find('td', {'data-stat': 'fta'}).text)
                except Exception:
                    fta = 0
                try:
                    ft = int(tr.find('td', {'data-stat': 'ft'}).text)
                except Exception:
                    ft = 0
                try:
                    stl = int(tr.find('td', {'data-stat': 'stl'}).text)
                except Exception:
                    stl = 0
                try:
                    blk = int(tr.find('td', {'data-stat': 'blk'}).text)
                except Exception:
                    blk = 0
                try:
                    tov = int(tr.find('td', {'data-stat': 'tov'}).text)
                except Exception:
                    tov = 0
                try:
                    plus_minus = int(tr.find('td', {'data-stat': 'plus_minus'}).text)
                except Exception:
                    plus_minus = 0

            else:
                up = False
                format_playing_time = '0 minutes 0 seconds'
                pts = oreb = dreb = reb = ast = fg = fga = fg3 = fg3a = ft = fta = stl = blk = tov = plus_minus = 0
            regular_data.append((name, year, date_game, up, format_playing_time, pts, reb, oreb,
                                 dreb, ast, fga, fg, fg3a, fg3, fta, ft, stl, blk, tov, plus_minus,
                                 team, opp, game_win))
            # print(f"{season}赛季数据获取完毕")
            # print(
            #     f"日期:{date_game},选手：{player_name},上场时间：{format_playing_time},母队：{team},对手：{opp},game_id:{game_id},是否上场：{up}")
            # print(
            #     f"得分:{pts},篮板：{oreb}-{dreb}-{reb}，助攻：{ast}，投篮：{fg}/{fga}，三分球：{fg3}/{fg3a}，罚球：{ft}/{fta}，抢断：{stl}，盖帽：{blk}，失误：{tov}，正负值：{plus_minus}")
    else:
        print("Table with id='pgl_basic' not found on the page")
    if regular_data:
        sql = """
        INSERT INTO public.player_regular_gamelog ("player_name", "season","game_date","up", "playing_time","pts", "reb","oreb","dreb","ast", "fga","fg", "fg3a","fg3", "fta","ft","stl","blk", "tov","plus_minus","team", "opp","game_win")
            VALUES (%s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """
        store_to_db(sql,regular_data)

    # try:
    #     playoffs_table = soup.find('table', {'id': 'pgl_basic_playoffs'})
    # except Exception:
    #     return
    # playoffs_data = []
    # if playoffs_table:
    #     tbody = playoffs_table.find('tbody')
    #     tr_tags = tbody.find_all('tr')
    #     for tr in tr_tags:
    #         if tr.get('class') and 'thead' in tr.get('class'):
    #             continue
    #         date_game = tr.find('td', {'data-stat': 'date_game'}).text
    #         team = tr.find('td', {'data-stat': 'team_id'}).text
    #         opp = tr.find('td', {'data-stat': 'opp_id'}).text
    #         # game_id = tr.find('th', {'data-stat': 'ranker'}).text
    #         game_result = tr.find('td', {'data-stat': 'game_result'}).text
    #         game_win = True if game_result.split(" ")[0] == 'W' else False
    #         if tr.get('id') and tr.get('id').startswith('pgl_basic.'):
    #             up = True
    #             playing_time = tr.find('td', {'data-stat': 'mp'}).text
    #             split_playing_time = playing_time.split(":")
    #             try:
    #                 format_playing_time = f"{split_playing_time[0]} minutes {split_playing_time[1]} seconds"
    #             except Exception:
    #                 format_playing_time = '0 minutes 0 seconds'
    #             try:
    #                 pts = int(tr.find('td', {'data-stat': 'pts'}).text)
    #             except Exception:
    #                 pts = 0
    #             try:
    #                 oreb = int(tr.find('td', {'data-stat': 'orb'}).text)
    #             except Exception:
    #                 oreb = 0
    #             try:
    #                 dreb = int(tr.find('td', {'data-stat': 'drb'}).text)
    #             except Exception:
    #                 dreb = 0
    #             try:
    #                 reb = int(tr.find('td', {'data-stat': 'trb'}).text)
    #             except Exception:
    #                 reb = 0
    #             try:
    #                 ast = int(tr.find('td', {'data-stat': 'ast'}).text)
    #             except Exception:
    #                 ast = 0
    #             try:
    #                 fga = int(tr.find('td', {'data-stat': 'fga'}).text)
    #             except Exception:
    #                 fga = 0
    #             try:
    #                 fg = int(tr.find('td', {'data-stat': 'fg'}).text)
    #             except Exception:
    #                 fg = 0
    #             try:
    #                 fg3a = int(tr.find('td', {'data-stat': 'fg3a'}).text)
    #             except Exception:
    #                 fg3a = 0
    #             try:
    #                 fg3 = int(tr.find('td', {'data-stat': 'fg3'}).text)
    #             except Exception:
    #                 fg3 = 0
    #             try:
    #                 fta = int(tr.find('td', {'data-stat': 'fta'}).text)
    #             except Exception:
    #                 fta = 0
    #             try:
    #                 ft = int(tr.find('td', {'data-stat': 'ft'}).text)
    #             except Exception:
    #                 ft = 0
    #             try:
    #                 stl = int(tr.find('td', {'data-stat': 'stl'}).text)
    #             except Exception:
    #                 stl = 0
    #             try:
    #                 blk = int(tr.find('td', {'data-stat': 'blk'}).text)
    #             except Exception:
    #                 blk = 0
    #             try:
    #                 tov = int(tr.find('td', {'data-stat': 'tov'}).text)
    #             except Exception:
    #                 tov = 0
    #             try:
    #                 plus_minus = int(tr.find('td', {'data-stat': 'plus_minus'}).text)
    #             except Exception:
    #                 plus_minus = 0

    #         else:
    #             up = False
    #             format_playing_time = '0 minutes 0 seconds'
    #             pts = oreb = dreb = reb = ast = fg = fga = fg3 = fg3a = ft = fta = stl = blk = tov = plus_minus = 0
    #         playoffs_data.append((name, year, date_game, up, format_playing_time, pts, reb, oreb,
    #                               dreb, ast, fga, fg, fg3a, fg3, fta, ft, stl, blk, tov, plus_minus,
    #                               team, opp, game_win))
    # else:
    #     print("Table with id='pgl_basic_playoffs' not found on the page")
    # # print(f"{season}赛季数据获取完毕")
    #
    # if playoffs_data:
    #     store_data_to_db(regular_data, 'player_playoffs_gamelog')



def get_user_info(url):
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        ths = soup.find_all('th', class_='left')
        datas = []
        for th in ths:
            name = th.find_next("a").text
            ulr_path = th.get('data-append-csv')
            start_year = th.find_next('td').text
            end_year = th.find_next('td').find_next('td').text
            # print(f"name:{name},url_path:{ulr_path},start_year:{start_year},end_year:{end_year}")
            datas.append({
                "name": name,
                "url_path": ulr_path,
                "start_year": int(start_year),
                "end_year": int(end_year),
            })
        return datas


if __name__ == '__main__':
    year = 2024

    where = "id>0"

    sql = f"""SELECT id,player_name,href FROM public.player_active where {where} ORDER BY id ASC;"""
    players = get_sql(sql)
    for player in players:
        player_name = player.get('player_name')
        player_url = player.get('href')
        if not player_url:
            continue
        player_id = player.get('id')

        player_url = f"https://www.basketball-reference.com{player_url.split('.')[0]}/gamelog/{year}"
        headers = {
            'authority': 'www.basketball-reference.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
            'cache-control': 'max-age=0',
            'cookie': 'UTDP=33%2C1%2C3%2C32%2C31%2C30; _pbjs_userid_consent_data=3524755945110770; cookie=60fdd009-12d8-45ce-960d-1db3b6d92008; _gcl_au=1.1.1218548003.1695192366; _cc_id=b6dff3962dd27312173d1f1330fb9719; __qca=P0-506589109-1695192358150; hubspotutk=260367dd23351173f284ac1b376486c3; _fbp=fb.1.1695192555964.297888169; sr_note_box_countdown=0; cf_clearance=OLkdYVHQ2DTBizJkJCo8uzM9xlVQGaMV.fllFVPZgak-1695725952-0-1-dca2d5df.2827ffdb.8ba38a3f-160.0.0; _au_1d=AU1D-0100-001696669265-OFBOJMVK-ZOG9; sr_n=3%7CMon%2C%2009%20Oct%202023%2004%3A01%3A18%20GMT; is_live=true; __hssrc=1; panoramaId_expiry=1698126366921; panoramaId=2c02b52d376669dae73a948be42a16d53938422e27b9484af4ab0e892bd3131e; panoramaIdType=panoIndiv; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%22ee153ffb-e206-47b9-b349-411a6bfede43%22; srcssfull=yes; _gid=GA1.2.521324283.1697698278; cto_bundle=f20pSV93QlJoNTloSHZsSmcwZGNJUGM3WFBwJTJCQ1FuWnNyaUNHbmVmJTJGWklpRUJ4bjlaY25kViUyRkJnMFVTYTN3REk1bHI3VHE0TzRsbEN5RmQzWVR6JTJCR2FORm44Vks5NlJ2NXZtMTlXMW5pbU9SQmpsSmxYek9IRFZ4UldjSmpUNGFWbzBuNUlZZ29wNzhLeDE4RVZSVzRBS2htQWxxSnk2RFBmR2wza1ElMkJiUFhLeUpZJTNE; __hstc=180814520.260367dd23351173f284ac1b376486c3.1695192546509.1697521553905.1697698437362.36; _au_last_seen_pixels=eyJhcG4iOjE2OTc2OTgyNzcsInR0ZCI6MTY5NzY5ODI3NywicHViIjoxNjk3Njk4Mjc3LCJydWIiOjE2OTc2OTgyNzcsInRhcGFkIjoxNjk3Njk4Mjc3LCJhZHgiOjE2OTc2OTgyNzcsImdvbyI6MTY5NzY5ODI3NywiYWRvIjoxNjk3Njk4ODY4LCJpbXByIjoxNjk3Njk4ODY4LCJzb24iOjE2OTc2OTg4NjgsIm9wZW54IjoxNjk3Njk4ODY4LCJwcG50IjoxNjk3Njk4ODY4LCJhbW8iOjE2OTc2OTgyNzcsImluZGV4IjoxNjk3Njk4ODY4LCJ1bnJ1bHkiOjE2OTc2OTg4NjgsInRhYm9vbGEiOjE2OTc2OTgyNzcsImJlZXMiOjE2OTc2OTg4NjgsInNtYXJ0IjoxNjk3Njk4Mjc3LCJjb2xvc3N1cyI6MTY5NzY5ODg2OH0=',
            # 'if-modified-since': 'Thu, 19 Oct 2023 06:15:41 GMT',
            'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
        }

        result = requests.get(player_url, headers=headers)
        if result.status_code != 200:
            print(result)
            sys.exit()
        response = result.text
        request_statics(response, player_name, year)
        print(f"player {player_id}:{player_name} {year} ok")

        random_number = random.randint(2, 4)
        time.sleep(random_number)
    print(f"{year}年所有运动员常规赛数据处理完毕")
