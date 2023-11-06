# -*- coding: utf-8 -*-
import os
import random
import markdown

import time
import traceback
from datetime import datetime, date

import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from bs4 import BeautifulSoup

from nba.image_utils import ImageUtils

old_rockets = [
    {
        'player_name': 'tyty_washington',
        'draft_position': 29,
        'name': '泰泰·华盛顿',
        'activity': False,
    },
    {
        'player_name': 'daishen_nix',
        'draft_position': '落选',
        'name': '戴申·尼克斯',
        'activity': False,
    },
    {
        'player_name': 'josh_christopher',
        'draft_position': 24,
        'name': '约什·克里斯托弗',
        'activity': False,
    },
    {
        'player_name': 'usman_garuba',
        'draft_position': 23,
        'name': '乌斯曼-加鲁巴',
        'activity': False,
    },
    {
        'player_name': 'kenyon_martin_jr',
        'draft_position': 52,
        'name': '小肯扬·马丁',
        'activity': False,
    },

]
rookies_2023 = [
    {
        'player_name': 'tmp_victor_wembanyama',
        'draft_position': "状元秀",
        'draft_year': 2023,
        'name': '维克托·文班亚马'
    }, {
        'player_name': 'brandon_miller',
        'draft_position': "榜眼秀",
        'draft_year': 2023,
        'name': '布兰登·米勒'
    }, {
        'player_name': 'scoot_henderson',
        'draft_position': "探花秀",
        'draft_year': 2023,
        'name': '斯库特·亨德森'
    }, {
        'player_name': 'amen_thompson',
        'draft_position': "4号秀",
        'draft_year': 2023,
        'name': '阿门·汤普森'
    }, {
        'player_name': 'ausar_thompson',
        'draft_position': "5号秀",
        'draft_year': 2023,
        'name': '奥萨尔·汤普森'
    },
    {
        'player_name': 'anthony_black',
        'draft_position': "6号秀",
        'draft_year': 2023,
        'name': '安东尼·布莱克'
    }, {
        'player_name': 'tmp_bilal_coulibaly',
        'draft_position': "7号秀",
        'draft_year': 2023,
        'name': '比拉尔·库利巴利'
    }, {
        'player_name': 'jarace_walker',
        'draft_position': "8号秀",
        'draft_year': 2023,
        'name': '贾雷斯·沃克'
    }, {
        'player_name': 'taylor_hendricks',
        'draft_position': "9号秀",
        'draft_year': 2023,
        'name': '泰勒·亨德里克斯'
    }, {
        'player_name': 'cason_wallace',
        'draft_position': "10号秀",
        'draft_year': 2023,
        'name': '卡森·华莱士'
    }, {
        'player_name': 'jett_howard',
        'draft_position': "11号秀",
        'draft_year': 2023,
        'name': '杰特·霍华德'
    }, {
        'player_name': 'dereck_lively_jr',
        'draft_position': "12号秀",
        'draft_year': 2023,
        'name': '德雷克·莱夫利二世'
    }, {
        'player_name': 'gradey_dick',
        'draft_position': "13号秀",
        'draft_year': 2023,
        'name': '格雷迪·迪克'
    }, {
        'player_name': 'jordan_hawkins',
        'draft_position': "14号秀",
        'draft_year': 2023,
        'name': '乔丹·霍金斯'
    }, {
        'player_name': 'kobe_bufkin',
        'draft_position': "15号秀",
        'draft_year': 2023,
        'name': '科比·巴夫金'
    }, {
        'player_name': 'keyonte_george',
        'draft_position': "16号秀",
        'draft_year': 2023,
        'name': '基扬特·乔治'
    }, {
        'player_name': 'jalen_hood-schifino',
        'draft_position': "17号秀",
        'draft_year': 2023,
        'name': '杰伦·胡德-希菲诺'
    }, {
        'player_name': 'jamie_jaquez_jr',
        'draft_position': "18号秀",
        'draft_year': 2023,
        'name': '小海梅·哈克斯'
    }, {
        'player_name': 'brandon_podziemski',
        'draft_position': "19号秀",
        'draft_year': 2023,
        'name': '布兰丁·波杰姆斯基'
    }, {
        'player_name': 'cam_whitmore',
        'draft_position': "20号秀",
        'draft_year': 2023,
        'name': '卡姆·惠特莫尔'
    }, {
        'player_name': 'noah_clowney',
        'draft_position': "21号秀",
        'draft_year': 2023,
        'name': '诺阿·克劳尼'
    }, {
        'player_name': 'dariq_whitehead',
        'draft_position': "22号秀",
        'draft_year': 2023,
        'name': '达里克·怀特海德'
    }, {
        'player_name': 'kris_murray',
        'draft_position': "23号秀",
        'draft_year': 2023,
        'name': '克里斯·默里'
    }, {
        'player_name': 'olivier-maxence_prosper',
        'draft_position': "24号秀",
        'draft_year': 2023,
        'name': '奥利维耶·马克萨斯-普洛斯珀'
    }, {
        'player_name': 'marcus_sasser',
        'draft_position': "25号秀",
        'draft_year': 2023,
        'name': '马库斯·萨瑟'
    }, {
        'player_name': 'ben_sheppard',
        'draft_position': "26号秀",
        'draft_year': 2023,
        'name': '本·谢泼德'
    }, {
        'player_name': 'nick_smith_jr',
        'draft_position': "27号秀",
        'draft_year': 2023,
        'name': '小尼克·史密斯'
    }, {
        'player_name': 'brice_sensabaugh',
        'draft_position': "28号秀",
        'draft_year': 2023,
        'name': '布赖斯·森萨博'
    }, {
        'player_name': 'julian_strawther',
        'draft_position': "29号秀",
        'draft_year': 2023,
        'name': '朱利安·斯特劳瑟'
    }, {
        'player_name': 'kobe_brown',
        'draft_position': "30号秀",
        'draft_year': 2023,
        'name': '科比·布朗'
    },
    #     {
    #     'player_name': 'james_naji',
    #     'draft_position': "31号秀",
    #     'draft_year': 2023,
    #     'name': '詹姆斯·纳吉'
    # },
    {
        'player_name': 'jalen_pickett',
        'draft_position': "32号秀",
        'draft_year': 2023,
        'name': '杰伦·皮克特'
    }, {
        'player_name': 'leonard_miller',
        'draft_position': "33号秀",
        'draft_year': 2023,
        'name': '伦纳德·米勒'
    }, {
        'player_name': 'colby_jones',
        'draft_position': "34号秀",
        'draft_year': 2023,
        'name': '科尔比·琼斯'
    }, {
        'player_name': 'julian_phillips',
        'draft_position': "35号秀",
        'draft_year': 2023,
        'name': '朱利安·菲利普斯'
    }, {
        'player_name': 'andre_jackson_jr',
        'draft_position': "36号秀",
        'draft_year': 2023,
        'name': '小安德烈·杰克逊'
    }, {
        'player_name': 'hunter_tyson',
        'draft_position': "37号秀",
        'draft_year': 2023,
        'name': '亨特·泰森'
    }, {
        'player_name': 'jordan_walsh',
        'draft_position': "38号秀",
        'draft_year': 2023,
        'name': '乔丹·沃尔什'
    }, {
        'player_name': 'mouhamed_gueye',
        'draft_position': "39号秀",
        'draft_year': 2023,
        'name': '穆罕穆德·古耶'
    }, {
        'player_name': 'maxwell_lewis',
        'draft_position': "40号秀",
        'draft_year': 2023,
        'name': '马克西·刘易斯'
    }, {
        'player_name': 'amari_bailey',
        'draft_position': "41号秀",
        'draft_year': 2023,
        'name': '阿马里·贝利'
    },
    #     {
    #     'player_name': 'tristan_vukcevic',
    #     'draft_position': "42号秀",
    #   'draft_year': 2023,
    #     'name': '特里斯坦·武切科维奇'
    # },
    {
        'player_name': 'rayan_rupert',
        'draft_position': "43号秀",
        'draft_year': 2023,
        'name': '拉扬·鲁伯特'
    }, {
        'player_name': 'sidy_cissoko',
        'draft_position': "44号秀",
        'draft_year': 2023,
        'name': '西迪·西索科'
    }, {
        'player_name': 'gg_jackson',
        'draft_position': "45号秀",
        'draft_year': 2023,
        'name': '格雷格·杰克逊'
    }, {
        'player_name': 'seth_lundy',
        'draft_position': "46号秀",
        'draft_year': 2023,
        'name': '塞斯·伦迪'
    },
    #     {
    #     'player_name': 'mojave_king',
    #     'draft_position': "47号秀",
    # 'draft_year': 2023,
    #     'name': '莫哈韦·金'
    # },
    {
        'player_name': 'jordan_miller',
        'draft_position': "48号秀",
        'draft_year': 2023,
        'name': '乔丹·米勒'
    }, {
        'player_name': 'emoni_bates',
        'draft_position': "49号秀",
        'draft_year': 2023,
        'name': '伊莫尼·贝茨'
    }, {
        'player_name': 'keyontae_johnson',
        'draft_position': "50号秀",
        'draft_year': 2023,
        'name': '基扬泰·约翰逊'
    }, {
        'player_name': 'jalen_wilson',
        'draft_position': "51号秀",
        'draft_year': 2023,
        'name': '杰伦·威尔逊'
    }, {
        'player_name': 'toumani_camara',
        'draft_position': "52号秀",
        'draft_year': 2023,
        'name': '图马尼·卡马拉'
    }, {
        'player_name': 'jaylen_clark',
        'draft_position': "53号秀",
        'draft_year': 2023,
        'name': '杰伦·克拉克'
    }, {
        'player_name': 'jalen_slawson',
        'draft_position': "54号秀",
        'draft_year': 2023,
        'name': '杰伦·斯劳森'
    }, {
        'player_name': 'isaiah_wong',
        'draft_position': "55号秀",
        'draft_year': 2023,
        'name': '以赛亚·王'
    },
    #     {
    #     'player_name': 'tarik_biberovic',
    #     'draft_position': "56号秀",
    #   'draft_year': 2023,
    #     'name': '塔里克·比贝洛维奇'
    # },
    {
        'player_name': 'trayce_jackson-davis',
        'draft_position': "57号秀",
        'draft_year': 2023,
        'name': '特雷斯·杰克逊·戴维斯'
    }, {
        'player_name': 'chris_livingston',
        'draft_position': "58号秀",
        'draft_year': 2023,
        'name': '克里斯·利文斯顿'
    }]
rookies_2022 = [
    {
        'player_name': 'paolo_banchero',
        'draft_position': "状元",
        'draft_year': 2022,
        'name': '保罗·班切罗'
    }, {
        'player_name': 'chet_holmgren',
        'draft_position': "榜眼",
        'draft_year': 2022,
        'name': '切特·霍姆格伦'
    }, {
        'player_name': 'jabari_smith',
        'draft_position': "探花",
        'draft_year': 2022,
        'name': '小贾巴里·史密斯'
    }, {
        'player_name': 'keegan_murray',
        'draft_position': "4号秀",
        'draft_year': 2022,
        'name': '基根·默里'
    }, {
        'player_name': 'jaden_ivey',
        'draft_position': "5号秀",
        'draft_year': 2022,
        'name': '杰登·艾维'
    }, {
        'player_name': 'tmp_bennedict_mathurin',
        'draft_position': "6号秀",
        'draft_year': 2022,
        'name': '本尼迪克特·马瑟林'
    }, {
        'player_name': 'shaedon_sharpe',
        'draft_position': "7号秀",
        'draft_year': 2022,
        'name': '谢登·夏普'
    }, {
        'player_name': 'dyson_daniels',
        'draft_position': "8号秀",
        'draft_year': 2022,
        'name': '戴森·丹尼尔斯'
    }, {
        'player_name': 'jeremy_sochan',
        'draft_position': "9号秀",
        'draft_year': 2022,
        'name': '杰里米·索汉'
    }, {
        'player_name': 'tmp_johnny_davis',
        'draft_position': "10号秀",
        'draft_year': 2022,
        'name': '约翰尼·戴维斯'
    }, {
        'player_name': 'ousmane_dieng',
        'draft_position': "11号秀",
        'draft_year': 2022,
        'name': '奥斯曼·吉昂'
    }, {
        'player_name': 'jalen_williams',
        'draft_position': "12号秀",
        'draft_year': 2022,
        'name': '杰伦·威廉姆斯'
    }, {
        'player_name': 'jalen_duren',
        'draft_position': "13号秀",
        'draft_year': 2022,
        'name': '杰伦·杜伦'
    }, {
        'player_name': 'ochai_agbaji',
        'draft_position': "14号秀",
        'draft_year': 2022,
        'name': '奥柴·阿巴基'
    }, {
        'player_name': 'mark_williams',
        'draft_position': "15号秀",
        'draft_year': 2022,
        'name': '马克·威廉姆斯'
    }, {
        'player_name': 'aj_griffin',
        'draft_position': "16号秀",
        'draft_year': 2022,
        'name': 'AJ·格里芬'
    }, {
        'player_name': 'tari_eason',
        'draft_position': "17号秀",
        'draft_year': 2022,
        'name': '塔里·伊森'
    }, {
        'player_name': 'dalen_terry',
        'draft_position': "18号秀",
        'draft_year': 2022,
        'name': '达伦·特里'
    }, {
        'player_name': 'jake_laravia',
        'draft_position': "19号秀",
        'draft_year': 2022,
        'name': '杰克·拉拉维亚'
    }, {
        'player_name': 'malaki_branham',
        'draft_position': "20号秀",
        'draft_year': 2022,
        'name': '马拉凯·布兰纳姆'
    }, {
        'player_name': 'christian_braun',
        'draft_position': "21号秀",
        'draft_year': 2022,
        'name': '克里斯蒂安·布劳恩'
    }, {
        'player_name': 'walker_kessler',
        'draft_position': "22号秀",
        'draft_year': 2022,
        'name': '沃克·凯斯勒'
    }, {
        'player_name': 'david_roddy',
        'draft_position': "23号秀",
        'draft_year': 2022,
        'name': '大卫·罗迪'
    }, {
        'player_name': 'marjon_beauchamp',
        'draft_position': "24号秀",
        'draft_year': 2022,
        'name': '马乔恩·比彻姆'
    }, {
        'player_name': 'blake_wesley',
        'draft_position': "25号秀",
        'draft_year': 2022,
        'name': '布雷克·韦斯利'
    }, {
        'player_name': 'wendell_moore',
        'draft_position': "26号秀",
        'draft_year': 2022,
        'name': '小温德尔·摩尔'
    }, {
        'player_name': 'nikola_jovic',
        'draft_position': "27号秀",
        'draft_year': 2022,
        'name': '尼科拉·约维奇'
    }, {
        'player_name': 'patrick_baldwin_jr',
        'draft_position': "28号秀",
        'draft_year': 2022,
        'name': '小帕特里克·鲍德温'
    }, {
        'player_name': 'tyty_washington',
        'draft_position': "29号秀",
        'draft_year': 2022,
        'name': '泰泰·华盛顿'
    }, {
        'player_name': 'peyton_watson',
        'draft_position': "30号秀",
        'draft_year': 2022,
        'name': '佩顿·沃特森'
    }, {
        'player_name': 'andrew_nembhard',
        'draft_position': "31号秀",
        'draft_year': 2022,
        'name': '安德鲁·内姆布哈德'
    }, {
        'player_name': 'caleb_houstan',
        'draft_position': "32号秀",
        'draft_year': 2022,
        'name': '凯莱布·休斯坦'
    }, {
        'player_name': 'christian_koloko',
        'draft_position': "33号秀",
        'draft_year': 2022,
        'name': '克里斯蒂安·科洛科'
    }, {
        'player_name': 'jaylin_williams',
        'draft_position': "34号秀",
        'draft_year': 2022,
        'name': '杰林·威廉姆斯'
    }, {
        'player_name': 'max_christie',
        'draft_position': "35号秀",
        'draft_year': 2022,
        'name': '马克斯·克里斯蒂'
    },
    #     {
    #     'player_name': 'gabriele_procida',
    #     'draft_position': "36号秀",
    # 'draft_year': 2022,
    #     'name': '加布里埃莱·普罗奇达'
    # },
    {
        'player_name': 'jaden_hardy',
        'draft_position': "37号秀",
        'draft_year': 2022,
        'name': '杰登·哈迪'
    },
    #     {
    #     'player_name': 'kennedy_chandler',
    #     'draft_position': "38号秀",
    # 'draft_year': 2022,
    #     'name': '肯尼迪·钱德勒'
    # },
    #     {
    #     'player_name': 'khalifa_diop',
    #     'draft_position': "39号秀",
    # 'draft_year': 2022,
    #     'name': '哈利法·迪奥普'
    # },
    {
        'player_name': 'bryce_mcgowens',
        'draft_position': "40号秀",
        'draft_year': 2022,
        'name': '布莱斯·麦戈文斯'
    }, {
        'player_name': 'ej_liddell',
        'draft_position': "41号秀",
        'draft_year': 2022,
        'name': 'E.J·利德尔'
    }, {
        'player_name': 'trevor_keels',
        'draft_position': "42号秀",
        'draft_year': 2022,
        'name': '特雷弗·基尔斯'
    }, {
        'player_name': 'tmp_moussa_diabate',
        'draft_position': "43号秀",
        'draft_year': 2022,
        'name': '穆萨·迪亚巴特'
    }, {
        'player_name': 'ryan_rollins',
        'draft_position': "44号秀",
        'draft_year': 2022,
        'name': '莱恩·罗林斯'
    }, {
        'player_name': 'josh_minott',
        'draft_position': "45号秀",
        'draft_year': 2022,
        'name': '约什·米诺特'
    },
    #     {
    #     'player_name': 'ismael_kamagate',
    #     'draft_position': "46号秀",
    #   'draft_year': 2022,
    #     'name': '伊斯梅尔·卡马盖特'
    # },
    {
        'player_name': 'vince_williams_jr',
        'draft_position': "47号秀",
        'draft_year': 2022,
        'name': '文斯·威廉姆斯'
    }, {
        'player_name': 'kendall_brown',
        'draft_position': "48号秀",
        'draft_year': 2022,
        'name': '肯德尔·布朗'
    }, {
        'player_name': 'isaiah_mobley',
        'draft_position': "49号秀",
        'draft_year': 2022,
        'name': '以赛亚·莫布利'
    },
    #     {
    #     'player_name': 'matteo_spagnolo',
    #     'draft_position': "50号秀",
    #   'draft_year': 2022,
    #     'name': '马泰奥·斯帕尼奥洛'
    # },
    {
        'player_name': 'tyrese_martin',
        'draft_position': "51号秀",
        'draft_year': 2022,
        'name': '泰雷斯·马丁'
    },
    # {
    #     'player_name': 'karlo_matkovic',
    #     'draft_position': "52号秀",
    #   'draft_year': 2022,
    #     'name': '卡洛·马特科维奇'
    # },
    {
        'player_name': 'jd_davison',
        'draft_position': "53号秀",
        'draft_year': 2022,
        'name': 'JD·戴维森'
    },
    # {
    #     'player_name': 'yannick_nzosa',
    #     'draft_position': "54号秀",
    #   'draft_year': 2022,
    #     'name': '扬尼克·恩佐萨'
    # },
    # {
    #     'player_name': 'gui_santos',
    #     'draft_position': "55号秀",
    #   'draft_year': 2022,
    #     'name': '古伊·桑托斯'
    # },
    # {
    #     'player_name': 'luke_travers',
    #     'draft_position': "56号秀",
    #   'draft_year': 2022,
    #     'name': '卢克·特拉弗斯'
    # },
    {
        'player_name': 'jabari_walker',
        'draft_position': "57号秀",
        'draft_year': 2022,
        'name': '贾巴里·沃克'
    },
    # {
    #     'player_name': 'hugo_besson',
    #     'draft_position': "58号秀",
    #   'draft_year': 2022,
    #     'name': '雨果·贝松'
    # }
]
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
young_stars = [
    {
        'player_name': 'tyrese_maxey',
        'name': '泰雷斯·马克西',
        'team': "76人",
        'draft_position': "2020年21顺位",
    },
    {
        'player_name': 'cade_cunningham',
        'name': '凯德·坎宁安',
        'team': "活塞",
        'draft_position': "2021年状元",
    },
    {
        'player_name': 'jalen_green',
        'name': '杰伦·格林',
        'team': "火箭",
        'draft_position': "2021年榜眼",
    },
    {
        'player_name': 'evan_mobley',
        'name': '埃文·莫布利',
        'team': "骑士",
        'draft_position': "2021年探花",
    },
    {
        'player_name': 'scottie_barnes',
        'name': '斯科蒂·巴恩斯',
        'team': "猛龙",
        'draft_position': "2021年4顺位",
    },
    {
        'player_name': 'josh_giddey',
        'name': '约什·吉迪',
        'team': "雷霆",
        'draft_position': "2021年6顺位",
    },
    {
        'player_name': 'franz_wagner',
        'name': '弗朗茨·瓦格纳',
        'team': "魔术",
        'draft_position': "2021年8顺位",
    },
    {
        'player_name': 'cam_thomas',
        'name': '卡梅伦·托马斯',
        'team': "篮网",
        'draft_position': "2020年21顺位",
    },
    {
        'player_name': 'paolo_banchero',
        'name': '保罗·班切罗',
        'team': "魔术",
        'draft_position': "2022年状元",
    },
    {
        'player_name': 'patrick_williams',
        'name': '帕特里克·威廉姆斯',
        'team': "公牛",
        'draft_position': "2020年4顺位",
    },
    {
        'player_name': 'alperen_sengun',
        'name': '阿尔佩伦·申京',
        'team': "火箭",
        'draft_position': "2021年16顺位",
    },
    {
        'player_name': 'jonathan_kuminga',
        'name': '乔纳森·库明加',
        'team': "勇士",
        'draft_position': "2021年7顺位",
    },
    {
        'player_name': 'jalen_suggs',
        'name': '杰伦·萨格斯',
        'team': "魔术",
        'draft_position': "2021年5顺位",
    },
    {
        'player_name': 'miles_bridges',
        'name': '迈尔斯·布里奇斯',
        'team': "黄蜂",
        'draft_position': "2018年12顺位",
    },
]

game_log = {}

file_path = "F:\\notebooks\\其他\\draft"


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
    for number in [475, 381, 379, 380]:
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
        random_number = random.randint(1, 3)
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
        player_datas = {}
        latest_games = data.get('payload', {}).get('player', {}).get('stats', {}).get('seasonGames')
        # print(latest_games)
        last_5_games = data.get('payload', {}).get('player', {}).get('stats', {}).get('playerSplit').get(
            'last5Games').get('statAverage')
        player_datas[
            'last_5_games'] = f"{last_5_games.get('pointsPg')}分 | {last_5_games.get('rebsPg')}篮板 | {last_5_games.get('assistsPg')}助攻 | {last_5_games.get('blocksPg')}盖帽 | {last_5_games.get('stealsPg')}抢断 | {last_5_games.get('turnoversPg')}失误"
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

                if min >= 6:
                    player_datas['result'] = f"{team} **{scores}** {opp}"
                    seconds = str(stat.get('secs')).zfill(2)
                    player_datas['time'] = f"上场时间：{min}:{seconds}"
                    pts = stat.get('points')
                    player_datas[
                        'name'] = f"{profile.get('teamProfile', {}).get('displayAbbr')}**{player.get('draft_position')}{player.get('name')}**"
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

                    eff = int(stat.get('efficiency'))
                    player_datas['eff'] = eff
                    player_datas['chinese_name'] = player.get('name')
                    player_datas['player_name'] = player.get('player_name')
                    player_datas['draft_year'] = player.get('draft_year')
                    player_datas['draft_position'] = player.get('draft_position')
                    player_datas['contract'] = player.get('contract')
                    player_datas['team'] = player.get('team')

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


def send_email(topic, msg):
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
    message.attach(MIMEText(msg, 'plain'))
    smtp_port = 465  # QQ邮箱的SMTP端口号

    # 请注意，您需要启用QQ邮箱的SMTP授权码，而不是QQ邮箱的登录密码
    smtp_username = '847634038@qq.com'
    smtp_password = 'yovtxvhipavhbcag'  # QQ邮箱的SMTP授权码

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


if __name__ == '__main__':
    today = datetime.now().strftime("%Y-%m-%d")

    stats_rookies_2023 = []
    stats_rookies_2022 = []
    stats_old_rockets = []
    stats_big_contracts = []
    stats_big_stars = []
    stats_young_guards = []
    for player in rookies_2023:
        try:
            stat_rookie_2023 = get_player_stats(player)
            if stat_rookie_2023:
                stats_rookies_2023.append(stat_rookie_2023)
        except Exception:
            print(f"err,{player.get('draft_position')}")

    sorted_rookies_2023 = sorted(stats_rookies_2023, key=lambda x: x['eff'], reverse=True)
    print(sorted_rookies_2023)
    tag = 'rookie_2023'
    file_name = os.path.join(file_path, f"{today}_rookie_2023.md")
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(
            f"北京时间：{today}，NBA比赛继续进行，今日共有{len(game_log.keys())}场比赛，{len(sorted_rookies_2023)}位新秀代表球队出战超过5分钟。\n\n")
        file.write(f"我们看看新秀们表现如何，按照表现好坏从差到好依次排序。\n\n")
        i = 1
        for player_data in sorted_rookies_2023:
            if i == 1:
                file.write(f"#### {i}. **今日之星**：{player_data.get('name')}\n")
            elif i == len(sorted_rookies_2023):
                file.write(f"#### {i}. **今日卧底**：{player_data.get('name')}\n")
            else:
                file.write(f"#### {i}. {player_data.get('name')}\n")

            file.write(
                f"![{player_data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{player_data.get('player_name')}_{tag}.png)\n\n")
            pd_str = ImageUtils().format_draw_data(player_data.get('player_name'), tag, player_data.get('hit_rate'),
                                                   player_data.get('data'))

            file.write(f"{player_data.get('time')}\n\n")

            file.write(f"数据：**{pd_str}**\n\n")
            file.write(f"{player_data.get('hit_rate')}\n\n")
            file.write(f"{player_data.get('result')}\n\n")
            file.write(f"近5场比赛：**{player_data.get('last_5_games')}**\n\n")

            
            file.write("---\n\n")
            i += 1

    for player in rookies_2022:
        try:
            stat_rookie_2022 = get_player_stats(player)
            if stat_rookie_2022:
                stats_rookies_2022.append(stat_rookie_2022)
        except Exception:
            print(f"err,{player.get('draft_position')}")

    sorted_rookies_2022 = sorted(stats_rookies_2022, key=lambda x: x['eff'], reverse=True)
    print(sorted_rookies_2022)
    today = datetime.now().strftime("%Y-%m-%d")
    tag = 'rookie_2022'
    file_name = os.path.join(file_path, f"{today}_rookie_2022.md")
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(
            "2022届新秀进入第二年，历史上的巨星们基本上在前两年就打出了名堂，我们看看今天二年级的新秀们表现如何。\n\n")
        file.write("**以下排名基于场上表现好坏，由差到好依次排列：**\n\n")
        i = 1
        for player_data in sorted_rookies_2022:
            if i == 1:
                file.write(f"#### {i}. **今日之星**：{player_data.get('name')}\n")
            elif i == len(sorted_rookies_2022):
                file.write(f"#### {i}. **今日卧底**：{player_data.get('name')}\n")
            else:
                file.write(f"#### {i}. {player_data.get('name')}\n")

            file.write(
                f"![{player_data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{player_data.get('player_name')}_{tag}.png)\n\n")
            pd_str = ImageUtils().format_draw_data(player_data.get('player_name'), tag, player_data.get('hit_rate'),
                                                   player_data.get('data'))

            file.write(f"{player_data.get('time')}\n\n")
            file.write(f"数据：**{pd_str}**\n\n")
            file.write(f"{player_data.get('hit_rate')}\n\n")
            file.write(f"{player_data.get('result')}\n\n")
            file.write(f"近5场比赛：**{player_data.get('last_5_games')}**\n\n")
            
            file.write("---\n\n")
            i += 1

    for player in old_rockets:
        try:
            stat_rocket = get_player_stats(player)
            if stat_rocket:
                stats_old_rockets.append(stat_rocket)
        except Exception as e:
            print(f"err,{player.get('draft_position')}")
            print(traceback.format_exc())
    print(stats_old_rockets)
    tag = 'old_rockets'
    file_name = os.path.join(file_path, f"{today}_old_rockets.md")
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(
            f"北京时间：{today}，NBA比赛继续进行，今日共有{len(stats_old_rockets)}名火箭旧将出战比赛，我们看看他们分别表现如何：\n\n")
        i = 1

        for player_data in stats_old_rockets:
            file.write(f"#### {i}. {player_data.get('chinese_name')}\n")
            file.write(
                f"![{player_data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{player_data.get('player_name')}_{tag}.png)\n\n")
            pd_str = ImageUtils().format_draw_data(player_data.get('player_name'), tag, player_data.get('hit_rate'),
                                                   player_data.get('data'))

            file.write(f"{player_data.get('time')}\n\n")
            file.write(f"数据：**{pd_str}**\n\n")
            file.write(f"{player_data.get('hit_rate')}\n\n")
            file.write(f"{player_data.get('result')}\n\n")
            file.write(f"近5场比赛：**{player_data.get('last_5_games')}**\n\n")
            
            file.write("---\n\n")
            i += 1

    for player in young_stars:
        try:
            stat_stars = get_player_stats(player)
            if stat_stars:
                stats_big_stars.append(stat_stars)
        except Exception as e:
            print(f"err,{player.get('draft_position')}")
            print(traceback.format_exc())
    sorted_stars = sorted(stats_big_stars, key=lambda x: x['eff'])
    print(sorted_stars)
    tag = 'young_stars'
    file_name = os.path.join(file_path, f"{today}_young_stars.md")
    with open(file_name, "w", encoding="utf-8") as file:
        i = 1
        for player_data in sorted_stars:
            if i == len(sorted_stars):
                file.write(f"#### {i}. **今日之星**：{player_data.get('chinese_name')}\n")
            else:
                file.write(f"#### {i}. {player_data.get('chinese_name')}\n")

            file.write(
                f"![{player_data.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{player_data.get('player_name')}_{tag}.png)\n\n")
            pd_str = ImageUtils().format_draw_data(player_data.get('player_name'), tag, player_data.get('hit_rate'),
                                                   player_data.get('data'))

            file.write(f"选秀：{player_data.get('team')}-**{player_data.get('draft_position')}**\n\n")
            file.write(f"{player_data.get('time')}\n\n")
            file.write(f"数据：**{pd_str}**\n\n")
            file.write(f"{player_data.get('hit_rate')}\n\n")

            file.write(f"比赛结果：{player_data.get('result')}\n\n")

            file.write(f"近5场比赛：**{player_data.get('last_5_games')}**\n\n")
            
            file.write("---\n\n")
            i += 1

