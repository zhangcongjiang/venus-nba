# -*- coding: utf-8 -*-
import os
import random
from email.mime.application import MIMEApplication

import markdown
import schedule
import time
import time
import traceback
from datetime import datetime, date

import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from bs4 import BeautifulSoup
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from tools.image_utils import ImageUtils
from tools.md_utils import md_to_doc
from tools.nba_utils import NbaUtils
from tools.sqlUtils import get_sql
from tools.table_utils import draw_table

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'Connection': 'keep-alive',
    'Cookie': 'privacyV2=true; _ga=GA1.2.902210438.1697680174; _ga_H1HTS9RJXW=GS1.2.1697680174.1.1.1697680248.0.0.0; AMCV_248F210755B762187F000101^%^40AdobeOrg=-1712354808^%^7CMCIDTS^%^7C19678^%^7CMCMID^%^7C48517773620589826003359889172843151504^%^7CMCAAMLH-1700801492^%^7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y^%^7CMCOPTOUT-1700203892s^%^7CNONE^%^7CMCAID^%^7CNONE^%^7CvVersion^%^7C4.3.0',
    'If-None-Match': '"3531-00f26cdf579447cab8aea22f8d7aa1da20a27525"',
    'Referer': 'https://china.nba.cn/articles/licensee_widget_scoreboard.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}

game_log = {}

file_path = "F:\\notebooks\\其他\\draft"
csv_path = "F:\\pycharm_workspace\\venus\\nba\\csv"

table_path = "F:\\pycharm_workspace\\venus\\nba\\game_tables"

nba_utils = NbaUtils()

today = datetime.now().strftime("%Y-%m-%d")
topics = []


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
                scores = f"{profile.get('teamScore')}：{profile.get('oppTeamScore')}"
                win_or_loss = profile.get('winOrLoss')
                is_home = profile.get('isHome')
                if team not in game_log.keys() and opp not in game_log.keys():
                    game_log[team] = f"{team} {scores} {'战胜' if win_or_loss == 'Won' else '不敌'}{opp}"

                stat = game.get('statTotal', {})
                min = int(stat.get('mins'))

                if min >= 12:
                    player_datas['result'] = f"{team} **{scores}** {opp}"
                    seconds = str(stat.get('secs')).zfill(2)
                    player_datas['time'] = (min, seconds)
                    pts = stat.get('points')
                    rebs = int(stat.get('rebs'))
                    asts = int(stat.get('assists'))
                    blks = int(stat.get('blocks'))
                    stls = int(stat.get('steals'))
                    tov = int(stat.get('turnovers'))
                    player_datas['data'] = (
                        pts,
                        rebs,
                        asts,
                        stls,
                        blks,
                        tov
                    )
                    if win_or_loss == 'Won':
                        player_datas['score'] = sum(player_datas['data'][:5]) + 5 - int(player_datas['data'][5])
                    else:
                        player_datas['score'] = sum(player_datas['data'][:5]) - 5 - int(player_datas['data'][5])
                    player_datas['hit_rate'] = (
                        stat.get('fgm'), stat.get('fga'), stat.get('tpm'), stat.get('tpa'), stat.get('ftm'),
                        stat.get('fta'))
                    print(player_datas)
                    return player_datas

    else:
        print('Failed to retrieve data. Status code:', response.status_code)


def send_email(topic, file_path):
    # 设置发件人和收件人的邮箱地址
    sender_email = '847634038@qq.com'
    receiver_email = '847634038@qq.com'

    # 创建邮件内容
    subject = topic

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # 添加文本内容
    msg = "This is the body of the email."
    message.attach(MIMEText(msg, 'plain'))
    smtp_port = 465  # QQ邮箱的SMTP端口号

    # 请注意，您需要启用QQ邮箱的SMTP授权码，而不是QQ邮箱的登录密码
    smtp_username = '847634038@qq.com'
    smtp_password = 'yovtxvhipavhbcag'  # QQ邮箱的SMTP授权码

    with open(file_path, 'rb') as file:
        attachment = MIMEApplication(file.read(), Name='file.txt')
        attachment['Content-Disposition'] = f'attachment; filename={file_path}'
        message.attach(attachment)
    # 连接到SMTP服务器
    with smtplib.SMTP_SSL('smtp.qq.com', smtp_port) as server:
        server.login(smtp_username, smtp_password)  # 登录到SMTP服务器
        server.sendmail(sender_email, receiver_email, message.as_string())


def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        markdown_content = file.read()
        # 将Markdown内容解析为纯文本
        html_content = markdown.markdown(markdown_content)
        # 使用HTML解析器将HTML内容转换为纯文本
        plain_text = ''.join(BeautifulSoup(html_content, "html.parser").findAll(text=True))
        return plain_text


def today_games():
    if not os.path.exists(f"F:\\adoc\\{today}"):
        os.mkdir(f"F:\\adoc\\{today}")
    response = requests.get('https://china.nba.cn/stats2/scores/miniscoreboardlive.json', headers=headers, verify=False)
    teams = []
    if response.status_code == 200:
        data = response.json()
        if not data:
            return
        games = data.get('payload', {}).get('today', {}).get('games', [])

        for game in games:
            game_id = game.get('profile', {}).get('gameId')
            away_rank = f"{game.get('awayTeam', {}).get('matchup', {}).get('wins')}胜{game.get('awayTeam', {}).get('matchup', {}).get('losses')}负，排名{game.get('awayTeam', {}).get('profile', {}).get('displayConference')}第{game.get('awayTeam', {}).get('matchup', {}).get('confRank')}"

            home_rank = f"{game.get('homeTeam', {}).get('matchup', {}).get('wins')}胜{game.get('homeTeam', {}).get('matchup', {}).get('losses')}负，排名{game.get('homeTeam', {}).get('profile', {}).get('displayConference')}第{game.get('homeTeam', {}).get('matchup', {}).get('confRank')}"
            game_statics(game_id, home_rank, away_rank)

    else:
        print("获取今天的比赛失败")
    return teams


def game_statics(game_id, home_rank, away_rank):
    url = f"https://china.nba.cn/stats2/game/snapshotlive.json?countryCode=CN&gameId={game_id}&locale=zh_CN&tz=%2B8"
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:

        data = response.json()
        if data.get('payload', {}).get('boxscore', {}).get("statusDesc") != '结束':
            return
        arena = data.get('payload', {}).get('gameProfile', {}).get('arenaName')
        home = data.get('payload', {}).get('homeTeam', {}).get('profile', {}).get('city')
        home_en = data.get('payload', {}).get('homeTeam', {}).get('profile', {}).get('abbr')
        home_team = data.get('payload', {}).get('homeTeam', {}).get('profile', {}).get('displayAbbr')
        home_score = data.get('payload', {}).get('boxscore', {}).get("homeScore")
        home_players = data.get('payload', {}).get('homeTeam', {}).get('gamePlayers')

        sorted_home_players = []
        start_home_players = sorted(home_players[:5], key=lambda x: x.get('statTotal', {}).get('points'), reverse=True)
        bench_home_players = sorted(home_players[5:], key=lambda x: x.get('statTotal', {}).get('points'), reverse=True)
        sorted_home_players.extend(start_home_players)
        sorted_home_players.extend(bench_home_players)
        data_to_csv(sorted_home_players, game_id, home_team)

        home_top = sorted(home_players,
                          key=lambda x: x.get('statTotal', {}).get('points') + x.get('statTotal', {}).get('rebs') + x.get('statTotal', {}).get(
                              'assists'), reverse=True)

        away_players = data.get('payload', {}).get('awayTeam', {}).get('gamePlayers')
        away = data.get('payload', {}).get('awayTeam', {}).get('profile', {}).get('city')
        away_en = data.get('payload', {}).get('awayTeam', {}).get('profile', {}).get('abbr')
        away_team = data.get('payload', {}).get('awayTeam', {}).get('profile', {}).get('displayAbbr')
        away_score = data.get('payload', {}).get('boxscore', {}).get("awayScore")

        sorted_away_players = []
        start_away_players = sorted(away_players[:5], key=lambda x: x.get('statTotal', {}).get('points'), reverse=True)
        bench_away_players = sorted(away_players[5:], key=lambda x: x.get('statTotal', {}).get('points'), reverse=True)
        sorted_away_players.extend(start_away_players)
        sorted_away_players.extend(bench_away_players)
        data_to_csv(sorted_away_players, game_id, away_team)
        away_top = sorted(away_players,
                          key=lambda x: x.get('statTotal', {}).get('points') + x.get('statTotal', {}).get('rebs') + x.get('statTotal', {}).get(
                              'assists'), reverse=True)

        file_name = os.path.join(file_path, f"{today}_{home_team}vs{away_team}.md")
        with open(file_name, "w", encoding="utf-8") as file:
            score_gap = home_score - away_score
            if score_gap > 20:
                game_result = "狂胜对手"
            elif score_gap > 5:
                game_result = "战胜对手"
            elif score_gap > 0:
                game_result = "险胜对手"
            elif score_gap > -5:
                game_result = "遗憾败北"
            elif score_gap > -20:
                game_result = "不敌对手"
            else:
                game_result = "遭遇吊打"
            file.write(
                f"北京时间{today}，{home}{home_team}坐镇{arena}迎战{away}{away_team}，本场比赛之前，{home_team}{home_rank}，{away_team}{away_rank}。\n\n")
            file.write(f"双方首发阵容如下：\n")
            file.write(f"{home_team}队：")
            home_starts = []
            for start in start_home_players:
                home_starts.append(start.get('profile', {}).get('displayName').replace(" ", "·").replace("贾伦", "杰伦").replace("'", "''"))
            file.write("、".join(home_starts))
            file.write(";\n")
            file.write(f"{away_team}队：")
            away_starts = []
            for start in start_away_players:
                away_starts.append(start.get('profile', {}).get('displayName').replace(" ", "·").replace("贾伦", "杰伦").replace("'", "''"))
            file.write("、".join(away_starts))
            file.write("。\n\n")
            file.write(
                f"最终全场战罢，{home_team}以**{home_score}：{away_score}**在主场{game_result}。\n\n")
            file.write(f"个人数据上，{home_team}球员表现如下：\n")
            i = 0
            for p in home_top[:4]:
                player_name = p.get('profile', {}).get('displayName').replace(" ", "·").replace(" ", "·").replace("贾伦", "杰伦").replace("'", "''")
                pts = p.get('statTotal', {}).get('points')
                rebs = p.get('statTotal', {}).get('rebs')
                asts = p.get('statTotal', {}).get('assists')
                stls = p.get('statTotal', {}).get('steals')
                blks = p.get('statTotal', {}).get('blocks')
                file.write(
                    f"{player_name}{p.get('statTotal', {}).get('fga')}投{p.get('statTotal', {}).get('fgm')}中，")
                if p.get('statTotal', {}).get('tpm') >= 2:
                    file.write(f"其中三分球{p.get('statTotal', {}).get('tpa')}中{p.get('statTotal', {}).get('tpm')}，")
                file.write(f"贡献{pts}分")
                if rebs > 0:
                    file.write(f"{rebs}篮板")
                if asts > 0:
                    file.write(f"{asts}助攻")
                if stls > 0:
                    file.write(f"{stls}抢断")
                if blks > 0:
                    file.write(f"{blks}盖帽")
                if i < 3:
                    file.write("；\n\n")
                    hit_rate = f"投篮：{p.get('statTotal', {}).get('fgm')}/{p.get('statTotal', {}).get('fga')} | 三分：{p.get('statTotal', {}).get('tpm')}/{p.get('statTotal', {}).get('tpa')} | 罚球：{p.get('statTotal', {}).get('ftm')}/{p.get('statTotal', {}).get('fta')}"
                    ImageUtils().body_img(p.get('profile', {}).get('displayNameEn').replace(' ', '_'),
                                          (

                                              f"{p.get('statTotal', {}).get('points')}", "Pts",
                                              f"{p.get('statTotal', {}).get('rebs')}", "Reb",
                                              f"{p.get('statTotal', {}).get('assists')}", "Ast",
                                              f"{p.get('statTotal', {}).get('steals')}", "Stl",
                                              f"{p.get('statTotal', {}).get('blocks')}", "Blk",
                                              f"{p.get('statTotal', {}).get('turnovers')}", "Tov",
                                          ), hit_rate, home_en, 'daily', i)
                    file.write(
                        f"![](F:\\pycharm_workspace\\venus\\nba\\body_img\\{p.get('profile', {}).get('displayNameEn').replace(' ', '_')}_{home_en}_daily_{i}.png)\n\n")

                else:
                    file.write("。\n\n")
                i += 1

            file.write(f"{away_team}方面：\n")
            i = 0
            for p in away_top[:4]:
                player_name = p.get('profile', {}).get('displayName').replace(" ", "·").replace("贾伦", "杰伦").replace("'", "''")
                pts = p.get('statTotal', {}).get('points')
                rebs = p.get('statTotal', {}).get('rebs')
                asts = p.get('statTotal', {}).get('assists')
                stls = p.get('statTotal', {}).get('steals')
                blks = p.get('statTotal', {}).get('blocks')
                file.write(
                    f"{player_name}{p.get('statTotal', {}).get('fga')}投{p.get('statTotal', {}).get('fgm')}中，")
                if p.get('statTotal', {}).get('tpm') >= 2:
                    file.write(f"其中三分球{p.get('statTotal', {}).get('tpa')}中{p.get('statTotal', {}).get('tpm')}，")
                file.write(f"贡献{pts}分")
                if rebs > 0:
                    file.write(f"{rebs}篮板")
                if asts > 0:
                    file.write(f"{asts}助攻")
                if stls > 0:
                    file.write(f"{stls}抢断")
                if blks > 0:
                    file.write(f"{blks}盖帽")
                if i < 3:
                    file.write("；\n\n")
                    hit_rate = f"投篮：{p.get('statTotal', {}).get('fgm')}/{p.get('statTotal', {}).get('fga')} | 三分：{p.get('statTotal', {}).get('tpm')}/{p.get('statTotal', {}).get('tpa')} | 罚球：{p.get('statTotal', {}).get('ftm')}/{p.get('statTotal', {}).get('fta')}"
                    ImageUtils().body_img(p.get('profile', {}).get('displayNameEn').replace(' ', '_'),
                                          (

                                              f"{p.get('statTotal', {}).get('points')}", "Pts",
                                              f"{p.get('statTotal', {}).get('rebs')}", "Reb",
                                              f"{p.get('statTotal', {}).get('assists')}", "Ast",
                                              f"{p.get('statTotal', {}).get('steals')}", "Stl",
                                              f"{p.get('statTotal', {}).get('blocks')}", "Blk",
                                              f"{p.get('statTotal', {}).get('turnovers')}", "Tov",
                                          ), hit_rate, away_en, 'daily', i)
                    file.write(
                        f"![](F:\\pycharm_workspace\\venus\\nba\\body_img\\{p.get('profile', {}).get('displayNameEn').replace(' ', '_')}_{away_en}_daily_{i}.png)\n\n")

                else:
                    file.write("。\n\n")
                i += 1
            file.write("\n\n")
            file.write(f"{home_team}队全场技术统计如下：\n\n")
            file.write(f"![]({table_path}\\{game_id}_{home_team}.png)\n\n")
            file.write(f"{away_team}队全场技术统计如下：\n\n")
            file.write(f"![]({table_path}\\{game_id}_{away_team}.png)\n\n")
        # doc_name = f"F:\\adoc\\{today}\\{today}_{home_team}vs{away_team}.docx"
        # md_to_doc(file_name, doc_name)
        # topic = f"{today}_{home_team}vs{away_team}"
        # if topic not in topics:
        #     topics.append(topic)
        #     send_email(topic, doc_name)
        time.sleep(10)


def data_to_csv(players, game_id, tag):
    names = []
    pts = []
    rebs = []
    asts = []
    stls = []
    blks = []
    tovs = []
    plus_minus = []
    fg = []
    tp = []
    ft = []
    for p in players:
        name = p.get('profile', {}).get('displayName').replace(" ", "·").replace(" ", "·").replace("贾伦", "杰伦")
        names.append(name)
        pm = p.get('boxscore', {}).get('plusMinus')
        if int(pm) > 0:
            plus_minus.append(f"+{pm}")
        else:
            plus_minus.append(str(pm))
        pts.append(p.get('statTotal', {}).get('points'))
        rebs.append(p.get('statTotal', {}).get('rebs'))
        asts.append(p.get('statTotal', {}).get('assists'))
        stls.append(p.get('statTotal', {}).get('steals'))
        blks.append(p.get('statTotal', {}).get('blocks'))
        tovs.append(p.get('statTotal', {}).get('turnovers'))

        fg.append(f"{p.get('statTotal', {}).get('fgm')}/{p.get('statTotal', {}).get('fga')}")
        tp.append(f"{p.get('statTotal', {}).get('tpm')}/{p.get('statTotal', {}).get('tpa')}")
        ft.append(f"{p.get('statTotal', {}).get('ftm')}/{p.get('statTotal', {}).get('fta')}")
    data = pd.DataFrame(
        {
            "球员": names,
            "得分": pts,
            "篮板": rebs,
            "助攻": asts,
            "抢断": stls,
            "盖帽": blks,
            "失误": tovs,
            "两分球": fg,
            "三分球": tp,
            "罚球": ft,
            "正负值": plus_minus,
        }
    )
    csv_file = os.path.join(csv_path, f'{game_id}_{tag}.csv')
    data.to_csv(csv_file, index=False)
    draw_table(csv_file, game_id, tag)


if __name__ == '__main__':
    today_games()
