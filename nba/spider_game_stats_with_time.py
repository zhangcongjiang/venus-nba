# -*- coding: utf-8 -*-
import random
import time
import traceback
from datetime import datetime, date

import psycopg2
import requests

old_rockets = [
    {
        'player_name': 'tyty_washington',
        'draft_position': 29,
        'name': '泰泰·华盛顿'
    },
    {
        'player_name': 'daishen_nix',
        'draft_position': '落选',
        'name': '戴申·尼克斯'
    },
    {
        'player_name': 'josh_christopher',
        'draft_position': 24,
        'name': '约什·克里斯托弗'
    },
    {
        'player_name': 'usman_garuba',
        'draft_position': 23,
        'name': '乌斯曼-加鲁巴'
    },
    {
        'player_name': 'kenyon_martin_jr',
        'draft_position': 52,
        'name': '小肯扬·马丁'
    },
    {
        'player_name': 'kevin_porter_jr',
        'draft_position': 30,
        'name': '小凯文·波特'
    },
]
draft_2023 = [
    {
        'player_name': 'tmp_victor_wembanyama',
        'draft_position': 1,
        'name': '维克托·文班亚马'
    }, {
        'player_name': 'brandon_miller',
        'draft_position': 2,
        'name': '布兰登·米勒'
    }, {
        'player_name': 'scoot_henderson',
        'draft_position': 3,
        'name': '斯库特·亨德森'
    }, {
        'player_name': 'amen_thompson',
        'draft_position': 4,
        'name': '阿门·汤普森'
    }, {
        'player_name': 'ausar_thompson',
        'draft_position': 5,
        'name': '奥萨尔·汤普森'
    },
    {
        'player_name': 'anthony_black',
        'draft_position': 6,
        'name': '安东尼·布莱克'
    }, {
        'player_name': 'tmp_bilal_coulibaly',
        'draft_position': 7,
        'name': '比拉尔·库利巴利'
    }, {
        'player_name': 'jarace_walker',
        'draft_position': 8,
        'name': '贾雷斯·沃克'
    }, {
        'player_name': 'taylor_hendricks',
        'draft_position': 9,
        'name': '泰勒·亨德里克斯'
    }, {
        'player_name': 'cason_wallace',
        'draft_position': 10,
        'name': '卡森·华莱士'
    }, {
        'player_name': 'jett_howard',
        'draft_position': 11,
        'name': '杰特·霍华德'
    }, {
        'player_name': 'dereck_lively_jr',
        'draft_position': 12,
        'name': '德里克·莱夫利'
    }, {
        'player_name': 'gradey_dick',
        'draft_position': 13,
        'name': '格雷迪·迪克'
    }, {
        'player_name': 'jordan_hawkins',
        'draft_position': 14,
        'name': '乔丹·霍金斯'
    }, {
        'player_name': 'kobe_bufkin',
        'draft_position': 15,
        'name': '科比·巴夫金'
    }, {
        'player_name': 'keyonte_george',
        'draft_position': 16,
        'name': '基扬特·乔治'
    }, {
        'player_name': 'jalen_hood-schifino',
        'draft_position': 17,
        'name': '杰伦·胡德-希菲诺'
    }, {
        'player_name': 'jamie_jaquez_jr',
        'draft_position': 18,
        'name': '小海梅·哈克斯'
    }, {
        'player_name': 'brandon_podziemski',
        'draft_position': 19,
        'name': '布兰丁·波齐姆斯基'
    }, {
        'player_name': 'cam_whitmore',
        'draft_position': 20,
        'name': '卡姆·惠特莫尔'
    }, {
        'player_name': 'noah_clowney',
        'draft_position': 21,
        'name': '诺阿·克劳尼'
    }, {
        'player_name': 'dariq_whitehead',
        'draft_position': 22,
        'name': '达里克·怀特海德'
    }, {
        'player_name': 'kris_murray',
        'draft_position': 23,
        'name': '克里斯·穆雷'
    }, {
        'player_name': 'olivier-maxence_prosper',
        'draft_position': 24,
        'name': '奥利维耶·马克萨斯-普洛斯珀'
    }, {
        'player_name': 'marcus_sasser',
        'draft_position': 25,
        'name': '马库斯·萨瑟'
    }, {
        'player_name': 'ben_sheppard',
        'draft_position': 26,
        'name': '本·谢泼德'
    }, {
        'player_name': 'nick_smith_jr',
        'draft_position': 27,
        'name': '小尼克·史密斯'
    }, {
        'player_name': 'brice_sensabaugh',
        'draft_position': 28,
        'name': '布赖斯·森萨博'
    }, {
        'player_name': 'julian_strawther',
        'draft_position': 29,
        'name': '朱利安·斯特劳瑟'
    }, {
        'player_name': 'kobe_brown',
        'draft_position': 30,
        'name': '科比·布朗'
    },
    #     {
    #     'player_name': 'james_naji',
    #     'draft_position': 31,
    #     'name': '詹姆斯·纳吉'
    # },
    {
        'player_name': 'jalen_pickett',
        'draft_position': 32,
        'name': '杰伦·皮克特'
    }, {
        'player_name': 'leonard_miller',
        'draft_position': 33,
        'name': '伦纳德·米勒'
    }, {
        'player_name': 'colby_jones',
        'draft_position': 34,
        'name': '科尔比·琼斯'
    }, {
        'player_name': 'julian_phillips',
        'draft_position': 35,
        'name': '朱利安·菲利普斯'
    }, {
        'player_name': 'andre_jackson_jr',
        'draft_position': 36,
        'name': '小安德烈·杰克逊'
    }, {
        'player_name': 'hunter_tyson',
        'draft_position': 37,
        'name': '亨特·泰森'
    }, {
        'player_name': 'jordan_walsh',
        'draft_position': 38,
        'name': '乔丹·沃尔什'
    }, {
        'player_name': 'mouhamed_gueye',
        'draft_position': 39,
        'name': '穆罕穆德·古耶'
    }, {
        'player_name': 'maxwell_lewis',
        'draft_position': 40,
        'name': '马克西·刘易斯'
    }, {
        'player_name': 'amari_bailey',
        'draft_position': 41,
        'name': '阿马里·贝利'
    },
    #     {
    #     'player_name': 'tristan_vukcevic',
    #     'draft_position': 42,
    #     'name': '特里斯坦·武切科维奇'
    # },
    {
        'player_name': 'rayan_rupert',
        'draft_position': 43,
        'name': '拉扬·鲁伯特'
    }, {
        'player_name': 'sidy_cissoko',
        'draft_position': 44,
        'name': '西迪·西索科'
    }, {
        'player_name': 'gg_jackson',
        'draft_position': 45,
        'name': '格雷格·杰克逊'
    }, {
        'player_name': 'seth_lundy',
        'draft_position': 46,
        'name': '塞斯·伦迪'
    },
    #     {
    #     'player_name': 'mojave_king',
    #     'draft_position': 47,
    #     'name': '莫哈韦·金'
    # },
    {
        'player_name': 'jordan_miller',
        'draft_position': 48,
        'name': '乔丹·米勒'
    }, {
        'player_name': 'emoni_bates',
        'draft_position': 49,
        'name': '伊莫尼·贝茨'
    }, {
        'player_name': 'keyontae_johnson',
        'draft_position': 50,
        'name': '基扬泰·约翰逊'
    }, {
        'player_name': 'jalen_wilson',
        'draft_position': 51,
        'name': '杰伦·威尔逊'
    }, {
        'player_name': 'toumani_camara',
        'draft_position': 52,
        'name': '图马尼·卡马拉'
    }, {
        'player_name': 'jaylen_clark',
        'draft_position': 53,
        'name': '杰伦·克拉克'
    }, {
        'player_name': 'jalen_slawson',
        'draft_position': 54,
        'name': '杰伦·斯劳森'
    }, {
        'player_name': 'isaiah_wong',
        'draft_position': 55,
        'name': '以赛亚·王'
    },
    #     {
    #     'player_name': 'tarik_biberovic',
    #     'draft_position': 56,
    #     'name': '塔里克·比贝洛维奇'
    # },
    {
        'player_name': 'trayce_jackson-davis',
        'draft_position': 57,
        'name': '特雷斯.杰克逊·戴维斯'
    }, {
        'player_name': 'chris_livingston',
        'draft_position': 58,
        'name': '克里斯·利文斯顿'
    }]
draft_2022 = [
    {
        'player_name': 'paolo_banchero',
        'draft_position': 1,
        'name': '保罗·班切罗'
    }, {
        'player_name': 'chet_holmgren',
        'draft_position': 2,
        'name': '切特·霍姆格伦'
    }, {
        'player_name': 'jabari_smith',
        'draft_position': 3,
        'name': '小贾巴里·史密斯'
    }, {
        'player_name': 'keegan_murray',
        'draft_position': 4,
        'name': '基根·默里'
    }, {
        'player_name': 'jaden_ivey',
        'draft_position': 5,
        'name': '杰登·艾维'
    }, {
        'player_name': 'tmp_bennedict_mathurin',
        'draft_position': 6,
        'name': '本内迪克特·马图林'
    }, {
        'player_name': 'shaedon_sharpe',
        'draft_position': 7,
        'name': '谢登·夏普'
    }, {
        'player_name': 'dyson_daniels',
        'draft_position': 8,
        'name': '戴森·丹尼尔斯'
    }, {
        'player_name': 'jeremy_sochan',
        'draft_position': 9,
        'name': '杰里米·索汉'
    }, {
        'player_name': 'tmp_johnny_davis',
        'draft_position': 10,
        'name': '约翰尼·戴维斯'
    }, {
        'player_name': 'ousmane_dieng',
        'draft_position': 11,
        'name': '奥斯曼·吉昂'
    }, {
        'player_name': 'jalen_williams',
        'draft_position': 12,
        'name': '杰伦·威廉姆斯'
    }, {
        'player_name': 'jalen_duren',
        'draft_position': 13,
        'name': '杰伦·杜伦'
    }, {
        'player_name': 'ochai_agbaji',
        'draft_position': 14,
        'name': '奥柴·阿巴基'
    }, {
        'player_name': 'mark_williams',
        'draft_position': 15,
        'name': '马克·威廉姆斯'
    }, {
        'player_name': 'aj_griffin',
        'draft_position': 16,
        'name': 'AJ·格里芬'
    }, {
        'player_name': 'tari_eason',
        'draft_position': 17,
        'name': '塔里·伊森'
    }, {
        'player_name': 'dalen_terry',
        'draft_position': 18,
        'name': '达伦·特里'
    }, {
        'player_name': 'jake_laravia',
        'draft_position': 19,
        'name': '杰克·拉拉维亚'
    }, {
        'player_name': 'malaki_branham',
        'draft_position': 20,
        'name': '马拉凯·布兰纳姆'
    },
    {
        'player_name': 'christian_braun',
        'draft_position': 21,
        'name': '克里斯蒂安·布劳恩'
    }, {
        'player_name': 'walker_kessler',
        'draft_position': 22,
        'name': '沃克·凯斯勒'
    }, {
        'player_name': 'david_roddy',
        'draft_position': 23,
        'name': '大卫·罗迪'
    }, {
        'player_name': 'marjon_beauchamp',
        'draft_position': 24,
        'name': '马乔恩·比彻姆'
    }, {
        'player_name': 'blake_wesley',
        'draft_position': 25,
        'name': '布雷克·韦斯利'
    }, {
        'player_name': 'wendell_moore',
        'draft_position': 26,
        'name': '小温德尔·摩尔'
    }, {
        'player_name': 'nikola_jovic',
        'draft_position': 27,
        'name': '尼科拉·约维奇'
    }, {
        'player_name': 'patrick_baldwin_jr',
        'draft_position': 28,
        'name': '小帕特里克·鲍德温'
    }, {
        'player_name': 'tyty_washington',
        'draft_position': 29,
        'name': '泰泰·华盛顿'
    }, {
        'player_name': 'peyton_watson',
        'draft_position': 30,
        'name': '佩顿·沃特森'
    }, {
        'player_name': 'andrew_nembhard',
        'draft_position': 31,
        'name': '安德鲁·内姆布哈德'
    }, {
        'player_name': 'caleb_houstan',
        'draft_position': 32,
        'name': '凯莱布·休斯坦'
    }, {
        'player_name': 'christian_koloko',
        'draft_position': 33,
        'name': '克里斯蒂安·科洛科'
    }, {
        'player_name': 'jaylin_williams',
        'draft_position': 34,
        'name': '杰林·威廉姆斯'
    }, {
        'player_name': 'max_christie',
        'draft_position': 35,
        'name': '马克斯·克里斯蒂'
    },
    #     {
    #     'player_name': 'gabriele_procida',
    #     'draft_position': 36,
    #     'name': '加布里埃莱·普罗奇达'
    # },
    {
        'player_name': 'jaden_hardy',
        'draft_position': 37,
        'name': '杰登·哈迪'
    },
    #     {
    #     'player_name': 'kennedy_chandler',
    #     'draft_position': 38,
    #     'name': '肯尼迪·钱德勒'
    # },
    #     {
    #     'player_name': 'khalifa_diop',
    #     'draft_position': 39,
    #     'name': '哈利法·迪奥普'
    # },
    {
        'player_name': 'bryce_mcgowens',
        'draft_position': 40,
        'name': '布莱斯·麦戈文斯'
    }, {
        'player_name': 'ej_liddell',
        'draft_position': 41,
        'name': 'E.J·利德尔'
    },
    {
        'player_name': 'trevor_keels',
        'draft_position': 42,
        'name': '特雷弗·基尔斯'
    }, {
        'player_name': 'tmp_moussa_diabate',
        'draft_position': 43,
        'name': '穆萨·迪亚巴特'
    }, {
        'player_name': 'ryan_rollins',
        'draft_position': 44,
        'name': '莱恩·罗林斯'
    }, {
        'player_name': 'josh_minott',
        'draft_position': 45,
        'name': '约什·米诺特'
    },
    #     {
    #     'player_name': 'ismael_kamagate',
    #     'draft_position': 46,
    #     'name': '伊斯梅尔·卡马盖特'
    # },
    {
        'player_name': 'vince_williams_jr',
        'draft_position': 47,
        'name': '文斯·威廉姆斯'
    }, {
        'player_name': 'kendall_brown',
        'draft_position': 48,
        'name': '肯德尔·布朗'
    }, {
        'player_name': 'isaiah_mobley',
        'draft_position': 49,
        'name': '以赛亚·莫布利'
    },
    #     {
    #     'player_name': 'matteo_spagnolo',
    #     'draft_position': 50,
    #     'name': '马泰奥·斯帕尼奥洛'
    # },
    {
        'player_name': 'tyrese_martin',
        'draft_position': 51,
        'name': '泰雷斯·马丁'
    },
    # {
    #     'player_name': 'karlo_matkovic',
    #     'draft_position': 52,
    #     'name': '卡洛·马特科维奇'
    # },
    {
        'player_name': 'jd_davison',
        'draft_position': 53,
        'name': 'JD·戴维森'
    },
    # {
    #     'player_name': 'yannick_nzosa',
    #     'draft_position': 54,
    #     'name': '扬尼克·恩佐萨'
    # },
    # {
    #     'player_name': 'gui_santos',
    #     'draft_position': 55,
    #     'name': '古伊·桑托斯'
    # },
    # {
    #     'player_name': 'luke_travers',
    #     'draft_position': 56,
    #     'name': '卢克·特拉弗斯'
    # },
    {
        'player_name': 'jabari_walker',
        'draft_position': 57,
        'name': '贾巴里·沃克'
    },
    # {
    #     'player_name': 'hugo_besson',
    #     'draft_position': 58,
    #     'name': '雨果·贝松'
    # }
]
game_log = {}


class PsqlConnect:

    @staticmethod
    def connect(host, database, user, password, port):
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        return conn


def get_player_stats(player):
    random_number = random.randint(2, 5)
    time.sleep(random_number)
    url = f"http://china.nba.cn/stats2/player/stats.json?locale=zh_CN&playerCode={player.get('player_name')}"

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
        latest_games = data.get('payload', {}).get('player', {}).get('stats', {}).get('seasonGames')
        # print(latest_games)

        total_secs = total_pts = total_rebs = total_asts = total_blks = total_stls = total_tovs = total_effs = 0
        total_win = total_loss = 0
        total_fga = total_fg = total_fta = total_ft = total_fg3a = total_fg3 = 0
        best_match = -100
        total_match = 0
        player_datas = {'draft_position': player.get("draft_position"),
                        'chinese_name': player.get('name'),
                        'player_name': player.get('player_name')}

        for game in latest_games:
            date_start = "2023-10-24"
            formatted_date_start = datetime.strptime(date_start, "%Y-%m-%d").strftime("%Y-%m-%d")
            today = date.today().strftime("%Y-%m-%d")
            # print(f"今天时间：{today}")
            # 中美时间相差12小时
            game_date = int(game.get('profile', {}).get('utcMillis')) + 12 * 60 * 60 * 1000
            formatted_date = datetime.utcfromtimestamp(game_date / 1000).strftime('%Y-%m-%d')
            if today >= formatted_date > formatted_date_start:
                profile = game.get('profile')
                team = profile.get('teamProfile', {}).get('city') + profile.get('teamProfile', {}).get('displayAbbr')
                opp = profile.get('oppTeamProfile', {}).get('city') + profile.get('oppTeamProfile', {}).get(
                    'displayAbbr')
                scores = f"{profile.get('teamScore')}:{profile.get('oppTeamScore')}"
                win_or_loss = profile.get('winOrLoss')
                is_home = profile.get('isHome')
                match_result = f"{team} **{scores}** {'战胜' if win_or_loss == 'Won' else '不敌'}{opp}"
                if team not in game_log.keys() and opp not in game_log.keys():
                    game_log[team] = f"{team} {scores} {'战胜' if win_or_loss == 'Won' else '不敌'}{opp}"

                player_datas['team'] = team

                stat = game.get('statTotal', {})
                min = int(stat.get('mins'))

                if min:
                    total_match += 1

                    total_secs += 60 * min + int(stat.get('secs'))
                    total_pts += int(stat.get('points'))
                    total_rebs += int(stat.get('rebs'))
                    total_asts += int(stat.get('assists'))
                    total_stls += int(stat.get('steals'))
                    total_blks += int(stat.get('blocks'))
                    total_tovs += int(stat.get('turnovers'))

                    total_fga += int(stat.get('fga'))
                    total_fg += int(stat.get('fgm'))
                    total_fta += int(stat.get('fta'))
                    total_ft += int(stat.get('ftm'))
                    total_fg3a += int(stat.get('tpa'))
                    total_fg3 += int(stat.get('tpm'))

                    pts = stat.get('points')
                    data_detail = f"{pts}分"
                    rebs = int(stat.get('rebs'))
                    if rebs:
                        data_detail += f" | {rebs}篮板"
                    asts = int(stat.get('assists'))
                    if asts:
                        data_detail += f" | {asts}助攻"
                    blks = int(stat.get('blocks'))
                    if blks:
                        data_detail += f" | {blks}盖帽"
                    stls = int(stat.get('steals'))
                    if stls:
                        data_detail += f" | {stls}抢断"
                    tov = int(stat.get('turnovers'))

                    data_detail += f" | {tov}失误"
                    player_datas['match_result'] = match_result

                    eff = (pts + rebs + asts + blks + stls - tov * 1.5)
                    if eff > best_match:
                        best_match = eff
                        player_datas['data'] = data_detail
                    total_effs += eff

                    if win_or_loss == 'Won':
                        total_win += 1
                    else:
                        total_loss += 1
        if not total_match:
            return
        average_minutes = int(total_secs / (60 * total_match))
        average_seconds = (total_secs % (average_minutes * total_match)) / total_match

        player_datas['ave_time'] = "{:02d}:{:02d}".format(int(average_minutes), int(average_seconds))
        player_datas['ave_data'] = f" {round(total_pts / total_match, 1)}分 " \
                                   f"| {round(total_rebs / total_match, 1)}篮板 " \
                                   f"| {round(total_asts / total_match, 1)}助攻 " \
                                   f"| {round(total_stls / total_match, 1)}抢断 " \
                                   f"| {round(total_blks / total_match, 1)}盖帽 " \
                                   f"| {round(total_tovs / total_match, 1)}失误"

        if total_fga > 0:
            player_datas['ave_hit_rate'] = f"投篮{total_fg}/{total_fga}：{round(total_fg * 100 / total_fga, 1)}% "
        if total_fg3a > 0:
            player_datas[
                'ave_hit_rate'] += f"| 三分球{total_fg3}/{total_fg3a}：{round(total_fg3 * 100 / total_fg3a, 1)}% "
        if total_fta > 0:
            player_datas['ave_hit_rate'] += f"| 罚球{total_ft}/{total_fta}：{round(total_ft * 100 / total_fta, 1)}%"

        player_datas['won'] = total_win
        player_datas['loss'] = total_loss
        player_datas['eff'] = total_effs / total_match
        player_datas['total_match'] = total_match

        return player_datas

    else:
        print('Failed to retrieve data. Status code:', response.status_code)


if __name__ == '__main__':

    stats_2022 = []
    stats_2023 = []
    stats_old_rockets = []
    today = datetime.now().strftime("%Y-%m-%d")

    for player in draft_2022:

        try:
            stat_2022 = get_player_stats(player)
            if stat_2022:
                stats_2022.append(stat_2022)
        except Exception:
            print(f"err,{player.get('draft_position')}")

    sorted_2022 = sorted(stats_2022, key=lambda x: x['eff'], reverse=True)
    print(sorted_2022)

    file_name = f"F:\\notebooks\\其他\\draft\\{today}_2022_stats.md"
    with open(file_name, "w", encoding="utf-8") as file:
        # file.write(f"北京时间：{today}，NBA比赛继续进行，今日共有{len(game_log.keys())}场比赛：\n\n")
        # for result in game_log.values():
        #     file.write(f"* {result}\n\n")
        i = 1
        file.write("我们看看经过一个赛季的洗礼，二年级的球员们表现如何，哪些球员将在本赛季完成蜕变。以下排名有分先后：\n\n")
        for player_data in sorted_2022:
            file.write(f"#### {i}.{player_data.get('team')}{player_data.get('chinese_name')}\n")
            file.write(
                f"出战{player_data.get('total_match')}场比赛，{player_data.get('won')}胜{player_data.get('loss')}负，场均上场：{player_data.get('ave_time')}\n\n")
            file.write(f"选秀顺位：{player_data.get('draft_position')}\n\n")
            file.write(f"场均数据：{player_data.get('ave_data')}\n\n")
            file.write(f"命中率：{player_data.get('ave_hit_rate')}\n\n")

            file.write(f"最佳表现：{player_data.get('match_result')}的比赛中，贡献：{player_data.get('data')}\n\n")
            file.write(
                f"![{player_data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\img\\{player_data.get('player_name')}.png)\n\n")
            i += 1

    for player in draft_2023:
        if player.get('draft_position') > 30:
            try:
                stat_2023 = get_player_stats(player)
                if stat_2023:
                    stats_2023.append(stat_2023)
            except Exception:
                print(f"err,{player.get('draft_position')}")

    sorted_2023 = sorted(stats_2023, key=lambda x: x['eff'], reverse=True)
    print(sorted_2023)
    file_name = f"F:\\notebooks\\其他\\draft\\{today}_2023_stats.md"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write("我们看看2023届新秀们表现如何，排名有分先后：\n\n")
        i = 1

        for player_data in sorted_2023:
            file.write(f"#### {i}.{player_data.get('team')}{player_data.get('chinese_name')}\n")
            file.write(f"出战{player_data.get('total_match')}场比赛，场均上场：{player_data.get('ave_time')}\n\n")
            file.write(f"选秀顺位：{player_data.get('draft_position')}\n\n")
            file.write(f"场均数据：{player_data.get('ave_data')}\n\n")
            file.write(f"命中率：{player_data.get('ave_hit_rate')}\n\n")

            file.write(f"最佳表现：{player_data.get('match_result')}的比赛中，贡献：{player_data.get('data')}\n\n")
            file.write(
                f"![{player_data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\img\\{player_data.get('player_name')}.png)\n\n")
            i += 1

    for player in old_rockets:
        try:
            stat_rocket = get_player_stats(player)
            if stat_rocket:
                stats_old_rockets.append(stat_rocket)
        except Exception as e:
            print(f"err,{player.get('draft_position')}")
            print(traceback.format_exc())

    sorted_rocket = sorted(stats_old_rockets, key=lambda x: x['eff'], reverse=True)
    print(sorted_rocket)
    file_name = f"F:\\notebooks\\其他\\draft\\{today}_old_rockets_ststs.md"
    with open(file_name, "w", encoding="utf-8") as file:
        i = 1
        for player_data in sorted_rocket:
            file.write(f"#### {i}.{player_data.get('team')}{player_data.get('chinese_name')}\n")
            file.write(f"出战{player_data.get('total_match')}场比赛，场均上场：{player_data.get('ave_time')}\n\n")
            file.write(f"选秀顺位：{player_data.get('draft_position')}\n\n")
            file.write(f"场均数据：{player_data.get('ave_data')}\n\n")
            file.write(f"命中率：{player_data.get('ave_hit_rate')}\n\n")

            file.write(f"最佳表现：{player_data.get('match_result')}的比赛中，贡献：{player_data.get('data')}\n\n")
            file.write(
                f"![{player_data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\img\\{player_data.get('player_name')}.png)\n\n")
            i += 1
