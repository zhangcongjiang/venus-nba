# -*- coding: utf-8 -*-

import random
import time
import traceback
from datetime import datetime, date

import requests

from nba.sqlUtils import get_sql

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
rookies = [
    {
        'player_name': 'tmp_victor_wembanyama',
        'draft_position': 1,
        'draft_year': 2023,
        'name': '维克托·文班亚马'
    }, {
        'player_name': 'brandon_miller',
        'draft_position': 2,
        'draft_year': 2023,
        'name': '布兰登·米勒'
    }, {
        'player_name': 'scoot_henderson',
        'draft_position': 3,
        'draft_year': 2023,
        'name': '斯库特·亨德森'
    }, {
        'player_name': 'amen_thompson',
        'draft_position': 4,
        'draft_year': 2023,
        'name': '阿门·汤普森'
    }, {
        'player_name': 'ausar_thompson',
        'draft_position': 5,
        'draft_year': 2023,
        'name': '奥萨尔·汤普森'
    },
    {
        'player_name': 'anthony_black',
        'draft_position': 6,
        'draft_year': 2023,
        'name': '安东尼·布莱克'
    }, {
        'player_name': 'tmp_bilal_coulibaly',
        'draft_position': 7,
        'draft_year': 2023,
        'name': '比拉尔·库利巴利'
    }, {
        'player_name': 'jarace_walker',
        'draft_position': 8,
        'draft_year': 2023,
        'name': '贾雷斯·沃克'
    }, {
        'player_name': 'taylor_hendricks',
        'draft_position': 9,
        'draft_year': 2023,
        'name': '泰勒·亨德里克斯'
    }, {
        'player_name': 'cason_wallace',
        'draft_position': 10,
        'draft_year': 2023,
        'name': '卡森·华莱士'
    }, {
        'player_name': 'jett_howard',
        'draft_position': 11,
        'draft_year': 2023,
        'name': '杰特·霍华德'
    }, {
        'player_name': 'dereck_lively_jr',
        'draft_position': 12,
        'draft_year': 2023,
        'name': '德里克·莱夫利'
    }, {
        'player_name': 'gradey_dick',
        'draft_position': 13,
        'draft_year': 2023,
        'name': '格雷迪·迪克'
    }, {
        'player_name': 'jordan_hawkins',
        'draft_position': 14,
        'draft_year': 2023,
        'name': '乔丹·霍金斯'
    }, {
        'player_name': 'kobe_bufkin',
        'draft_position': 15,
        'draft_year': 2023,
        'name': '科比·巴夫金'
    }, {
        'player_name': 'keyonte_george',
        'draft_position': 16,
        'draft_year': 2023,
        'name': '基扬特·乔治'
    }, {
        'player_name': 'jalen_hood-schifino',
        'draft_position': 17,
        'draft_year': 2023,
        'name': '杰伦·胡德-希菲诺'
    }, {
        'player_name': 'jamie_jaquez_jr',
        'draft_position': 18,
        'draft_year': 2023,
        'name': '小海梅·哈克斯'
    }, {
        'player_name': 'brandon_podziemski',
        'draft_position': 19,
        'draft_year': 2023,
        'name': '布兰丁·波齐姆斯基'
    }, {
        'player_name': 'cam_whitmore',
        'draft_position': 20,
        'draft_year': 2023,
        'name': '卡姆·惠特莫尔'
    }, {
        'player_name': 'noah_clowney',
        'draft_position': 21,
        'draft_year': 2023,
        'name': '诺阿·克劳尼'
    }, {
        'player_name': 'dariq_whitehead',
        'draft_position': 22,
        'draft_year': 2023,
        'name': '达里克·怀特海德'
    }, {
        'player_name': 'kris_murray',
        'draft_position': 23,
        'draft_year': 2023,
        'name': '克里斯·穆雷'
    }, {
        'player_name': 'olivier-maxence_prosper',
        'draft_position': 24,
        'draft_year': 2023,
        'name': '奥利维耶·马克萨斯-普洛斯珀'
    }, {
        'player_name': 'marcus_sasser',
        'draft_position': 25,
        'draft_year': 2023,
        'name': '马库斯·萨瑟'
    }, {
        'player_name': 'ben_sheppard',
        'draft_position': 26,
        'draft_year': 2023,
        'name': '本·谢泼德'
    }, {
        'player_name': 'nick_smith_jr',
        'draft_position': 27,
        'draft_year': 2023,
        'name': '小尼克·史密斯'
    }, {
        'player_name': 'brice_sensabaugh',
        'draft_position': 28,
        'draft_year': 2023,
        'name': '布赖斯·森萨博'
    }, {
        'player_name': 'julian_strawther',
        'draft_position': 29,
        'draft_year': 2023,
        'name': '朱利安·斯特劳瑟'
    }, {
        'player_name': 'kobe_brown',
        'draft_position': 30,
        'draft_year': 2023,
        'name': '科比·布朗'
    },
    #     {
    #     'player_name': 'james_naji',
    #     'draft_position': 31,
    #     'draft_year': 2023,
    #     'name': '詹姆斯·纳吉'
    # },
    {
        'player_name': 'jalen_pickett',
        'draft_position': 32,
        'draft_year': 2023,
        'name': '杰伦·皮克特'
    }, {
        'player_name': 'leonard_miller',
        'draft_position': 33,
        'draft_year': 2023,
        'name': '伦纳德·米勒'
    }, {
        'player_name': 'colby_jones',
        'draft_position': 34,
        'draft_year': 2023,
        'name': '科尔比·琼斯'
    }, {
        'player_name': 'julian_phillips',
        'draft_position': 35,
        'draft_year': 2023,
        'name': '朱利安·菲利普斯'
    }, {
        'player_name': 'andre_jackson_jr',
        'draft_position': 36,
        'draft_year': 2023,
        'name': '小安德烈·杰克逊'
    }, {
        'player_name': 'hunter_tyson',
        'draft_position': 37,
        'draft_year': 2023,
        'name': '亨特·泰森'
    }, {
        'player_name': 'jordan_walsh',
        'draft_position': 38,
        'draft_year': 2023,
        'name': '乔丹·沃尔什'
    }, {
        'player_name': 'mouhamed_gueye',
        'draft_position': 39,
        'draft_year': 2023,
        'name': '穆罕穆德·古耶'
    }, {
        'player_name': 'maxwell_lewis',
        'draft_position': 40,
        'draft_year': 2023,
        'name': '马克西·刘易斯'
    }, {
        'player_name': 'amari_bailey',
        'draft_position': 41,
        'draft_year': 2023,
        'name': '阿马里·贝利'
    },
    #     {
    #     'player_name': 'tristan_vukcevic',
    #     'draft_position': 42,
    #   'draft_year': 2023,
    #     'name': '特里斯坦·武切科维奇'
    # },
    {
        'player_name': 'rayan_rupert',
        'draft_position': 43,
        'draft_year': 2023,
        'name': '拉扬·鲁伯特'
    }, {
        'player_name': 'sidy_cissoko',
        'draft_position': 44,
        'draft_year': 2023,
        'name': '西迪·西索科'
    }, {
        'player_name': 'gg_jackson',
        'draft_position': 45,
        'draft_year': 2023,
        'name': '格雷格·杰克逊'
    }, {
        'player_name': 'seth_lundy',
        'draft_position': 46,
        'draft_year': 2023,
        'name': '塞斯·伦迪'
    },
    #     {
    #     'player_name': 'mojave_king',
    #     'draft_position': 47,
    # 'draft_year': 2023,
    #     'name': '莫哈韦·金'
    # },
    {
        'player_name': 'jordan_miller',
        'draft_position': 48,
        'draft_year': 2023,
        'name': '乔丹·米勒'
    }, {
        'player_name': 'emoni_bates',
        'draft_position': 49,
        'draft_year': 2023,
        'name': '伊莫尼·贝茨'
    }, {
        'player_name': 'keyontae_johnson',
        'draft_position': 50,
        'draft_year': 2023,
        'name': '基扬泰·约翰逊'
    }, {
        'player_name': 'jalen_wilson',
        'draft_position': 51,
        'draft_year': 2023,
        'name': '杰伦·威尔逊'
    }, {
        'player_name': 'toumani_camara',
        'draft_position': 52,
        'draft_year': 2023,
        'name': '图马尼·卡马拉'
    }, {
        'player_name': 'jaylen_clark',
        'draft_position': 53,
        'draft_year': 2023,
        'name': '杰伦·克拉克'
    }, {
        'player_name': 'jalen_slawson',
        'draft_position': 54,
        'draft_year': 2023,
        'name': '杰伦·斯劳森'
    }, {
        'player_name': 'isaiah_wong',
        'draft_position': 55,
        'draft_year': 2023,
        'name': '以赛亚·王'
    },
    #     {
    #     'player_name': 'tarik_biberovic',
    #     'draft_position': 56,
    #   'draft_year': 2023,
    #     'name': '塔里克·比贝洛维奇'
    # },
    {
        'player_name': 'trayce_jackson-davis',
        'draft_position': 57,
        'draft_year': 2023,
        'name': '特雷斯.杰克逊·戴维斯'
    }, {
        'player_name': 'chris_livingston',
        'draft_position': 58,
        'draft_year': 2023,
        'name': '克里斯·利文斯顿'
    },
    {
        'player_name': 'paolo_banchero',
        'draft_position': 1,
        'draft_year': 2022,
        'name': '保罗·班切罗'
    }, {
        'player_name': 'chet_holmgren',
        'draft_position': 2,
        'draft_year': 2022,
        'name': '切特·霍姆格伦'
    }, {
        'player_name': 'jabari_smith',
        'draft_position': 3,
        'draft_year': 2022,
        'name': '小贾巴里·史密斯'
    }, {
        'player_name': 'keegan_murray',
        'draft_position': 4,
        'draft_year': 2022,
        'name': '基根·默里'
    }, {
        'player_name': 'jaden_ivey',
        'draft_position': 5,
        'draft_year': 2022,
        'name': '杰登·艾维'
    }, {
        'player_name': 'tmp_bennedict_mathurin',
        'draft_position': 6,
        'draft_year': 2022,
        'name': '本内迪克特·马图林'
    }, {
        'player_name': 'shaedon_sharpe',
        'draft_position': 7,
        'draft_year': 2022,
        'name': '谢登·夏普'
    }, {
        'player_name': 'dyson_daniels',
        'draft_position': 8,
        'draft_year': 2022,
        'name': '戴森·丹尼尔斯'
    }, {
        'player_name': 'jeremy_sochan',
        'draft_position': 9,
        'draft_year': 2022,
        'name': '杰里米·索汉'
    }, {
        'player_name': 'tmp_johnny_davis',
        'draft_position': 10,
        'draft_year': 2022,
        'name': '约翰尼·戴维斯'
    }, {
        'player_name': 'ousmane_dieng',
        'draft_position': 11,
        'draft_year': 2022,
        'name': '奥斯曼·吉昂'
    }, {
        'player_name': 'jalen_williams',
        'draft_position': 12,
        'draft_year': 2022,
        'name': '杰伦·威廉姆斯'
    }, {
        'player_name': 'jalen_duren',
        'draft_position': 13,
        'draft_year': 2022,
        'name': '杰伦·杜伦'
    }, {
        'player_name': 'ochai_agbaji',
        'draft_position': 14,
        'draft_year': 2022,
        'name': '奥柴·阿巴基'
    }, {
        'player_name': 'mark_williams',
        'draft_position': 15,
        'draft_year': 2022,
        'name': '马克·威廉姆斯'
    }, {
        'player_name': 'aj_griffin',
        'draft_position': 16,
        'draft_year': 2022,
        'name': 'AJ·格里芬'
    }, {
        'player_name': 'tari_eason',
        'draft_position': 17,
        'draft_year': 2022,
        'name': '塔里·伊森'
    }, {
        'player_name': 'dalen_terry',
        'draft_position': 18,
        'draft_year': 2022,
        'name': '达伦·特里'
    }, {
        'player_name': 'jake_laravia',
        'draft_position': 19,
        'draft_year': 2022,
        'name': '杰克·拉拉维亚'
    }, {
        'player_name': 'malaki_branham',
        'draft_position': 20,
        'draft_year': 2022,
        'name': '马拉凯·布兰纳姆'
    }, {
        'player_name': 'christian_braun',
        'draft_position': 21,
        'draft_year': 2022,
        'name': '克里斯蒂安·布劳恩'
    }, {
        'player_name': 'walker_kessler',
        'draft_position': 22,
        'draft_year': 2022,
        'name': '沃克·凯斯勒'
    }, {
        'player_name': 'david_roddy',
        'draft_position': 23,
        'draft_year': 2022,
        'name': '大卫·罗迪'
    }, {
        'player_name': 'marjon_beauchamp',
        'draft_position': 24,
        'draft_year': 2022,
        'name': '马乔恩·比彻姆'
    }, {
        'player_name': 'blake_wesley',
        'draft_position': 25,
        'draft_year': 2022,
        'name': '布雷克·韦斯利'
    }, {
        'player_name': 'wendell_moore',
        'draft_position': 26,
        'draft_year': 2022,
        'name': '小温德尔·摩尔'
    }, {
        'player_name': 'nikola_jovic',
        'draft_position': 27,
        'draft_year': 2022,
        'name': '尼科拉·约维奇'
    }, {
        'player_name': 'patrick_baldwin_jr',
        'draft_position': 28,
        'draft_year': 2022,
        'name': '小帕特里克·鲍德温'
    }, {
        'player_name': 'tyty_washington',
        'draft_position': 29,
        'draft_year': 2022,
        'name': '泰泰·华盛顿'
    }, {
        'player_name': 'peyton_watson',
        'draft_position': 30,
        'draft_year': 2022,
        'name': '佩顿·沃特森'
    }, {
        'player_name': 'andrew_nembhard',
        'draft_position': 31,
        'draft_year': 2022,
        'name': '安德鲁·内姆布哈德'
    }, {
        'player_name': 'caleb_houstan',
        'draft_position': 32,
        'draft_year': 2022,
        'name': '凯莱布·休斯坦'
    }, {
        'player_name': 'christian_koloko',
        'draft_position': 33,
        'draft_year': 2022,
        'name': '克里斯蒂安·科洛科'
    }, {
        'player_name': 'jaylin_williams',
        'draft_position': 34,
        'draft_year': 2022,
        'name': '杰林·威廉姆斯'
    }, {
        'player_name': 'max_christie',
        'draft_position': 35,
        'draft_year': 2022,
        'name': '马克斯·克里斯蒂'
    },
    #     {
    #     'player_name': 'gabriele_procida',
    #     'draft_position': 36,
    # 'draft_year': 2022,
    #     'name': '加布里埃莱·普罗奇达'
    # },
    {
        'player_name': 'jaden_hardy',
        'draft_position': 37,
        'draft_year': 2022,
        'name': '杰登·哈迪'
    },
    #     {
    #     'player_name': 'kennedy_chandler',
    #     'draft_position': 38,
    # 'draft_year': 2022,
    #     'name': '肯尼迪·钱德勒'
    # },
    #     {
    #     'player_name': 'khalifa_diop',
    #     'draft_position': 39,
    # 'draft_year': 2022,
    #     'name': '哈利法·迪奥普'
    # },
    {
        'player_name': 'bryce_mcgowens',
        'draft_position': 40,
        'draft_year': 2022,
        'name': '布莱斯·麦戈文斯'
    }, {
        'player_name': 'ej_liddell',
        'draft_position': 41,
        'draft_year': 2022,
        'name': 'E.J·利德尔'
    }, {
        'player_name': 'trevor_keels',
        'draft_position': 42,
        'draft_year': 2022,
        'name': '特雷弗·基尔斯'
    }, {
        'player_name': 'tmp_moussa_diabate',
        'draft_position': 43,
        'draft_year': 2022,
        'name': '穆萨·迪亚巴特'
    }, {
        'player_name': 'ryan_rollins',
        'draft_position': 44,
        'draft_year': 2022,
        'name': '莱恩·罗林斯'
    }, {
        'player_name': 'josh_minott',
        'draft_position': 45,
        'draft_year': 2022,
        'name': '约什·米诺特'
    },
    #     {
    #     'player_name': 'ismael_kamagate',
    #     'draft_position': 46,
    #   'draft_year': 2022,
    #     'name': '伊斯梅尔·卡马盖特'
    # },
    {
        'player_name': 'vince_williams_jr',
        'draft_position': 47,
        'draft_year': 2022,
        'name': '文斯·威廉姆斯'
    }, {
        'player_name': 'kendall_brown',
        'draft_position': 48,
        'draft_year': 2022,
        'name': '肯德尔·布朗'
    }, {
        'player_name': 'isaiah_mobley',
        'draft_position': 49,
        'draft_year': 2022,
        'name': '以赛亚·莫布利'
    },
    #     {
    #     'player_name': 'matteo_spagnolo',
    #     'draft_position': 50,
    #   'draft_year': 2022,
    #     'name': '马泰奥·斯帕尼奥洛'
    # },
    {
        'player_name': 'tyrese_martin',
        'draft_position': 51,
        'draft_year': 2022,
        'name': '泰雷斯·马丁'
    },
    # {
    #     'player_name': 'karlo_matkovic',
    #     'draft_position': 52,
    #   'draft_year': 2022,
    #     'name': '卡洛·马特科维奇'
    # },
    {
        'player_name': 'jd_davison',
        'draft_position': 53,
        'draft_year': 2022,
        'name': 'JD·戴维森'
    },
    # {
    #     'player_name': 'yannick_nzosa',
    #     'draft_position': 54,
    #   'draft_year': 2022,
    #     'name': '扬尼克·恩佐萨'
    # },
    # {
    #     'player_name': 'gui_santos',
    #     'draft_position': 55,
    #   'draft_year': 2022,
    #     'name': '古伊·桑托斯'
    # },
    # {
    #     'player_name': 'luke_travers',
    #     'draft_position': 56,
    #   'draft_year': 2022,
    #     'name': '卢克·特拉弗斯'
    # },
    {
        'player_name': 'jabari_walker',
        'draft_position': 57,
        'draft_year': 2022,
        'name': '贾巴里·沃克'
    },
    # {
    #     'player_name': 'hugo_besson',
    #     'draft_position': 58,
    #   'draft_year': 2022,
    #     'name': '雨果·贝松'
    # }
]
game_log = {}


def get_comments():
    hot_comments = {}
    url = 'https://games.mobileapi.hupu.com/1/8.0.1/bplcommentapi/bpl/score_tree/getCurAndSubNodeByBizKey'

    headers = {
        'authority': 'games.mobileapi.hupu.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
        'content-type': 'application/json',
        'cookie': 'Hm_lvt_4fac77ceccb0cd4ad5ef1be46d740615=1697519191; Hm_lvt_b241fb65ecc2ccf4e7e3b9601c7a50de=1697519191; smidV2=20230705134428aa0f3abb39776bbd16e7b26ece9eb6fa0065fd0c446c022b0; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218b3c073a0914c2-0385ef48d4f271e-26031151-2073600-18b3c073a0a117d%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThiM2MwNzNhMDkxNGMyLTAzODVlZjQ4ZDRmM2QxZS0yNjAzMTE1MS0yMDczNjAwLTE4YjNjMDczYTBhMTE3ZCJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218b3c073a0914c2-0385ef48d4f271e-26031151-2073600-18b3c073a0a117d%22%7D; Hm_lpvt_4fac77ceccb0cd4ad5ef1be46d740615=1697614977; Hm_lpvt_b241fb65ecc2ccf4e7e3b9601c7a50de=1697614977',
        'origin': 'https://offline-download.hupu.com',
        'referer': 'https://offline-download.hupu.com/',
        'reqid': 'de29af95-7b46-4fd0-b7c4-b8d85e925647',
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    }
    for number in [323, 324]:
        data = {
            "relation": "CHILD",
            "pageInfo": {"page": 1, "pageSize": 50},
            "outBizKey": {"outBizNo": f"{number}", "outBizType": "basketball_match"}
        }

        response = requests.post(url, headers=headers, json=data).json()
        if response.get('code') == 1:
            datas = response.get('data', {}).get('pageResult', {}).get('data', [])
            for data in datas:
                name = data.get('node', {}).get('name', '').replace('-', '·')
                hot_comment = data.get('node', {}).get('hottestComments')[0] if len(
                    data.get('node', {}).get('hottestComments')) else '暂无热评，等你发挥'

                hot_comments[name] = hot_comment
        random_number = random.randint(2, 4)
        time.sleep(random_number)
    return hot_comments


def get_player_stats(player):
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
                scores = f"{profile.get('teamScore')}:{profile.get('oppTeamScore')}"
                win_or_loss = profile.get('winOrLoss')
                is_home = profile.get('isHome')
                if team not in game_log.keys() and opp not in game_log.keys():
                    game_log[team] = f"{team} {scores} {'战胜' if win_or_loss == 'Won' else '不敌'}{opp}"

                stat = game.get('statTotal', {})
                min = int(stat.get('mins'))

                if min > 3:
                    player_datas = {'result': f"{team} **{scores}** {opp}"}
                    seconds = str(stat.get('secs')).zfill(2)
                    player_datas['time'] = f"上场时间：{min}:{seconds}"

                    pts = stat.get('points')
                    player_datas[
                        'name'] = f"{profile.get('teamProfile', {}).get('displayAbbr')}**{player.get('draft_year')}年{player.get('draft_position')}**号秀**{player.get('name')}**"
                    player_datas['data'] = f"数据：{pts}分"
                    rebs = int(stat.get('rebs'))
                    if rebs:
                        player_datas['data'] = player_datas['data'] + f" | {rebs}篮板"
                    asts = int(stat.get('assists'))
                    if asts:
                        player_datas['data'] = player_datas['data'] + f" | {asts}助攻"
                    blks = int(stat.get('blocks'))
                    if blks:
                        player_datas['data'] = player_datas['data'] + f" | {blks}盖帽"
                    stls = int(stat.get('steals'))
                    if stls:
                        player_datas['data'] = player_datas['data'] + f" | {stls}抢断"
                    tov = int(stat.get('turnovers'))

                    player_datas['data'] = player_datas['data'] + f" | {tov}失误"
                    eff = int(stat.get('efficiency'))
                    player_datas['eff'] = eff
                    player_datas['chinese_name'] = player.get('name')
                    player_datas['player_name'] = player.get('player_name')

                    if int(stat.get('fga')):
                        fg = f"{stat.get('fgm')}/{stat.get('fga')}"
                        player_datas['hit_rate'] = f"投篮：{fg}"
                        if int(stat.get('tpa')):
                            fg3 = f"{stat.get('tpm')}/{stat.get('tpa')}"

                            player_datas['hit_rate'] = player_datas['hit_rate'] + f" | 三分球：{fg3}"
                        if int(stat.get('fta')):
                            ft = f"{stat.get('ftm')}/{stat.get('fta')}"
                            player_datas['hit_rate'] = player_datas['hit_rate'] + f" | 罚球：{ft}"
                    else:
                        player_datas['hit_rate'] = '出手次数为0'

                    return player_datas

    else:
        print('Failed to retrieve data. Status code:', response.status_code)


if __name__ == '__main__':
    sql = """
        SELECT id, player_id, code, player_name, chinese_name, draft_year, draft_position, team, team_en, height, body_weight, "position"
FROM public.player_active;
    """

    players = get_sql(sql)
    for player in players:
        try:
            stat_rookie = get_player_stats(player)
            if stat_rookie:
                stats_rookies.append(stat_rookie)
        except Exception:
            print(f"err,{player.get('draft_position')}")

    sorted_rookies = sorted(stats_rookies, key=lambda x: x['eff'], reverse=True)
    print(sorted_rookies)
    today = datetime.now().strftime("%Y-%m-%d")

    file_name = f"F:\\notebooks\\其他\\draft\\{today}_rookie.md"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(f"北京时间：{today}，NBA比赛继续进行，今日共有{len(game_log.keys())}场比赛：\n\n")
        for result in game_log.values():
            file.write(f"* {result}\n\n")
        i = 1
        file.write(
            "新秀是球队的未来，勇士、掘金、凯尔特人、雄鹿等球队依靠选秀走向争冠之路，火箭、雷霆、魔术、马刺等通过摆烂选到了多位潜力新星意图东山再起。我们看看今天新秀们的表现如何，以下排名有分先后，包含一年级新秀和二年级新秀：\n\n")
        for player_data in sorted_rookies:
            file.write(f"#### {i}. {player_data.get('name')}\n")
            file.write(f"{player_data.get('time')}\n\n")
            file.write(f"{player_data.get('data')}\n\n")
            file.write(f"{player_data.get('hit_rate')}\n\n")

            file.write(
                f"![{player_data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\img\\{player_data.get('player_name')}.png)\n\n")
            file.write(f"网友热评：{hot_comments.get(player_data.get('chinese_name'))}\n\n")
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
    file_name = f"F:\\notebooks\\其他\\draft\\{today}_old_rockets.md"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(
            f"北京时间：{today}，NBA比赛继续进行，今日共有{len(sorted_rocket)}名火箭旧将出战比赛，我们看看他们分别表现如何：\n\n")
        i = 1

        for player_data in sorted_rocket:
            file.write(f"#### {i}. {player_data.get('chinese_name')}\n")
            file.write(f"{player_data.get('time')}\n\n")
            file.write(f"{player_data.get('data')}\n\n")
            file.write(f"{player_data.get('hit_rate')}\n\n")
            file.write(f"{player_data.get('result')}\n\n")
            file.write(
                f"![{player_data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\img\\{player_data.get('player_name')}.png)\n\n")
            file.write(f"网友热评：{hot_comments.get(player_data.get('chinese_name'))}\n\n")
            i += 1