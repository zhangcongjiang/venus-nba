import os
import random
from PIL import Image, ImageDraw, ImageFont
import textwrap

from tools.nba_utils import NbaUtils

SRC_PATH = 'F:\\pycharm_workspace\\venus\\nba\\image'
DST_PATH = 'F:\\pycharm_workspace\\venus\\nba\\dataimg'


class ImageUtils:

    def paste(self, src, dst):
        image1 = Image.open(dst)

        # make a copy the image so that the
        # original image does not get affected
        image1copy = image1.copy()
        image2 = Image.open(src)
        image2copy = image2.copy()
        image2copy = self.circle_corner(image2copy, 50)
        image1copy.paste(image2copy, (20, 20))

        image1copy.save('pasted2.png')

    def circle_corner(self, img, radii):  # 把原图片变成圆角，这个函数是从网上找的，原址 https://www.pyget.cn/p/185266
        """
        圆角处理
        :param img: 源图象。
        :param radii: 半径，如：30。
        :return: 返回一个圆角处理后的图象。
        """

        # 画圆（用于分离4个角）
        circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建一个黑色背景的画布
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 画白色圆形
        # 原图
        img = img.convert("RGBA")
        w, h = img.size
        # 画4个角（将整圆分离为4个部分）
        alpha = Image.new('L', img.size, 255)
        alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
        alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
        alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角
        alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角
        # alpha.show()
        img.putalpha(alpha)  # 白色区域透明可见，黑色区域不可见
        return img

    def draw_text(self, img_name, team, tag, hit_rate, data, num):
        font_path = 'simhei.ttf'
        if not team:
            team = ''
        detail_files = sorted([file for file in os.listdir(SRC_PATH) if file.startswith(img_name + "_" + team)])
        if detail_files:
            img = random.choice(detail_files)
        else:
            files = sorted([file for file in os.listdir(SRC_PATH) if file.startswith(img_name)])
            if files:
                img = files[-1]
            else:
                img = os.path.join(SRC_PATH, "nba.png")
        img_file = os.path.join(SRC_PATH, img)
        img = Image.open(img_file)
        width, height = img.size
        spacing = int((height - 100) / len(data))
        font_size = spacing - 20
        if font_size > 60:
            font_size = 60
            spacing = 84
        font1 = ImageFont.truetype(font_path, font_size)
        font2 = ImageFont.truetype(font_path, int(0.5 * font_size))
        background_color = '#74615a'
        logo_font = ImageFont.truetype(font_path, 24)
        # 在图片上添加文字
        draw = ImageDraw.Draw(img)
        i = 0
        for txt in data:
            fill = '#ffffff'

            if i == 0:
                x = 900
                draw.text((50, font_size), text='星佳期', font=logo_font, fill='#808080')
                draw.text((x, i * spacing), text=txt, font=font1, fill=fill)
            elif i == len(data) - 1:
                x = 960 + font_size * 3 + 25
                draw.text((x, i * spacing), text=txt, font=font1, fill=fill)
            else:
                x = 960
                draw.rectangle([x - 10, i * spacing - 5, x + font_size * 3 + 20, i * spacing + font_size + 5],
                               fill=background_color)  # 设置背景色
                txt1, txt2 = txt.split(" ")[0], txt.split(" ")[1]
                draw.text((x, i * spacing), text=txt1, font=font1, fill=fill)
                draw.text((x + 20 + font_size * len(txt1) / 2, i * spacing + 0.5 * font_size), text=txt2, font=font2,
                          fill=fill)

            i += 1
        logo_x = 1000
        logo_y = height - 100

        draw.text((logo_x, logo_y), text='星佳期原创', font=logo_font, fill='#808080')

        hit_rate_font = ImageFont.truetype(font_path, 28)
        hit_rate_x = 1100 - len(hit_rate.split("|")) * 150
        draw.rectangle([hit_rate_x - 10, height - 50 - 5, x + spacing + 10, height - 50 + 28 + 5],
                       fill=background_color)  # 设置背景色
        draw.text((hit_rate_x, height - 50), text=hit_rate, font=hit_rate_font, fill='#ffffff')
        file = os.path.join(DST_PATH, img_name)
        if not team:
            team = 'None'
        img.save(f"{file}_{team}_{tag}_{num}.png")

    def format_draw_data(self, name, team, tag, hit_rate, data, i):
        pd_list = ['┏']
        pd = []
        for key, value in data.items():
            if value != 0:
                pd_list.append(key)
                pd_list.append(f"{value}")
                pd.append(f'{value}{key}')
        pd_str = " | ".join(pd).replace("得", "").replace("：", "")
        pd_list.append('┛')
        self.draw_text(name, team, tag, hit_rate, tuple(pd_list), i)
        return pd_str

    def body_img(self, name, datas, hit_rate, team, tag, num):
        name = name.replace("'", "")
        body_path = f"./../nba/logo/{name}_body.png"
        if not os.path.exists(body_path):
            body_path = "./../nba/logo/None_body.png"
        img = Image.open(body_path)

        # 获取图片的尺寸
        width, height = img.size
        background_color = '#2b2b2b'
        # 创建新的图片，尺寸为440*700，背景色与原图一致
        new_img = Image.new('RGBA', (width + 160, height + 100), color=(0, 0, 0, 0))

        # 创建Draw对象，用于绘制文字和矩形框
        draw = ImageDraw.Draw(new_img)

        # 定义字体和文字大小，你需要替换为适合你的字体和大小
        score_font = ImageFont.truetype("verdana.ttf", 48)
        desc_font = ImageFont.truetype('simhei.ttf', 24)

        # 在图片下方添加矩形框，
        draw.rectangle((0, height + 100, width + 160, height + 100), fill=(0, 0, 0, 0))
        # 图片右侧矩形框
        draw.rectangle((width, 0, width + 160, height + 100), fill=(0, 0, 0, 0))

        # 计算文字宽度

        mask = desc_font.getmask(hit_rate)
        text_width = mask.size[0]

        # 在下方矩形框中添加文字，起始位置为(220 - text_width/2, height-75)，字体为前面定义的字体
        draw.text((580 - text_width, height + 30), hit_rate, font=desc_font, fill=background_color)
        new_img.paste(img, (0, 0))

        font_size = 36
        spacing = 30
        txt_height = 100
        fill = '#ffffff'
        background_color = '#74615a'

        scores = datas[::2]
        longest_score = max(scores, key=len)
        mask = score_font.getmask(longest_score)
        text_width = mask.size[0]
        draw.text((450 - text_width, spacing * 2 + txt_height), text="┏", font=desc_font, fill=background_color)

        i = 0
        for txt in datas:

            if i == 0:
                mask = score_font.getmask(txt)
                text_width = mask.size[0]
                draw.text((30, font_size), text='星佳期', font=desc_font, fill='#808080')

                draw.text((500 - text_width, (i + 3) * spacing + txt_height), text=txt, font=score_font, fill=background_color)
            elif i % 2 == 1:
                x = 520
                draw.text((x, (i + 2) * spacing + txt_height + 18), text=txt, font=desc_font, fill=background_color)
            else:
                mask = score_font.getmask(txt)
                text_width = mask.size[0]
                draw.text((500 - text_width, (i + 3) * spacing + txt_height), text=txt, font=score_font, fill=background_color)

            i += 1

        draw.text((560, (spacing) * (i + 3) + txt_height), text="┛", font=desc_font, fill=background_color)

        # 保存新图片

        # 在图片外围绘制白色outline
        border_color = (255, 255, 255, 255)  # 红色outline的RGBA颜色值

        # 上边框
        draw.line([(0, 0), (width + 159, 0)], fill=border_color, width=1)
        # 下边框
        draw.line([(0, height + 99), (width + 159, height + 99)], fill=border_color, width=1)
        # 左边框
        draw.line([(0, 0), (0, height + 99)], fill=border_color, width=1)
        # 右边框
        draw.line([(width + 159, 0), (width + 159, height + 99)], fill=border_color, width=1)
        save_path = f"./../nba/body_img/{name.replace(' ', '_')}_{team}_{tag}_{num}.png"
        new_img.save(save_path)

    def long_img(self, players, tag):
        head_font = ImageFont.truetype("simhei.ttf", 64)
        desc_font = ImageFont.truetype('simhei.ttf', 24)
        stress_font = ImageFont.truetype('simhei.ttf', 32)
        num = len(players)
        msg_len = len(players[0].get('extra'))
        long_img = Image.new('RGBA', (450 * num, 900 + msg_len * 50), color=(0, 0, 0, 0))
        i = num
        dpi = 300
        for player in players:

            new_img = Image.new('RGBA', (440, 900 + msg_len * 50), color=(0, 0, 0, 0))
            body_path = f"./../nba/logo/{player.get('player_name').replace(' ', '_').split('-')[0]}_body.png"
            img = Image.open(body_path)
            new_img.paste(img, (0, 0))
            # 创建Draw对象，用于绘制文字和矩形框
            draw = ImageDraw.Draw(new_img)

            draw.rectangle((0, 700, 440, 900 + msg_len * 50), fill='black')
            index_num = str(i)
            mask = stress_font.getmask(index_num)
            text_width = mask.size[0]
            draw.text((80 - text_width / 2, 50), text=index_num, font=head_font, fill='white')

            # 重点突出内容
            stress = player.get('stress')
            mask = stress_font.getmask(stress)
            text_width = mask.size[0]
            draw.text((220 - text_width / 2, 715), stress, font=stress_font, fill='yellow')

            # 中文名
            chinese_name = player.get('chinese_name')
            mask = desc_font.getmask(chinese_name)
            text_width = mask.size[0]
            draw.text((220 - text_width / 2, 785), chinese_name, font=desc_font, fill='white')

            # 额外信息
            lines = player.get('extra')
            line_num = 0
            for line in lines:
                mask = desc_font.getmask(line)
                text_width = mask.size[0]
                draw.text((220 - text_width / 2, 830 + line_num * 40), line, font=desc_font, fill='white')
                line_num += 1
            if i >= num - 3:
                logo_img = new_img.resize((int(440 * dpi / 100), int((900 + msg_len * 50) * dpi / 100)), resample=Image.LANCZOS)
                logo_img.save(f"./../nba/images/{tag}_{num - i + 1}.png", dpi=(dpi, dpi))

            long_img.paste(new_img, ((num - i) * 450, 0))
            i -= 1
        save_path = f"./../nba/images/{tag}.png"
        long_img = long_img.resize((int((450 * num) * dpi / 100), int((900 + msg_len * 50) * dpi / 100)), resample=Image.LANCZOS)

        long_img.save(save_path, dpi=(dpi, dpi))


if __name__ == '__main__':
    player_list = ['LeBron James', 'Stephen Curry', 'Victor Wembanyama', 'Nikola Jokic', 'Luka Doncic', 'Jayson Tatum', 'Kevin Durant',
                   'Jimmy Butler', 'Giannis Antetokounmpo', 'Jamal Murray',
                   'Anthony Davis', 'Kyrie Irving', 'Austin Reaves', 'Joel Embiid', 'Ja Morant']

    datas = {}
    hitrates = {}
    for player in player_list:
        result = NbaUtils().get_game_log_with_season(player, 2024)
        data = f"{result.get('this_data')[0]}分{result.get('this_data')[1]}篮板{result.get('this_data')[2]}助攻{result.get('this_data')[3]}抢断{result.get('this_data')[4]}盖帽"
        hitrate = f"投篮：{round(result.get('this_hit_rate')[0] * 100 / result.get('this_hit_rate')[1], 1)}% 三分：{round(result.get('this_hit_rate')[2] * 100 / result.get('this_hit_rate')[3], 1)}% 罚球：{round(result.get('this_hit_rate')[4] * 100 / result.get('this_hit_rate')[5], 1)}%"
        datas[player.replace(" ", "_")] = data
        hitrates[player.replace(" ", "_")] = hitrate

    players = [
        {
            "player_name": 'LeBron_James',
            "chinese_name": "勒布朗·詹姆斯",
            "stress": "28.0亿次",
            "extra": [datas.get('LeBron_James'), hitrates.get('LeBron_James')]
        },
        {
            "player_name": 'Stephen_Curry',
            "chinese_name": "斯蒂芬·库里",
            "stress": "16.0亿次",
            "extra": [datas.get('Stephen_Curry'), hitrates.get('Stephen_Curry')]
        },
        {
            "player_name": 'Victor_Wembanyama',
            "chinese_name": "维克托·文班亚马",
            "stress": "13.0亿次",
            "extra": [datas.get('Victor_Wembanyama'), hitrates.get('Victor_Wembanyama')]
        },
        {
            "player_name": 'Nikola_Jokic',
            "chinese_name": "尼古拉·约基奇",
            "stress": "12.0亿次",
            "extra": [datas.get('Nikola_Jokic'), hitrates.get('Nikola_Jokic')]
        },
        {
            "player_name": 'Luka_Doncic',
            "chinese_name": "卢卡·东契奇",
            "stress": "9.14亿次",
            "extra": [datas.get('Luka_Doncic'), hitrates.get('Luka_Doncic')]
        },
        {
            "player_name": 'Jayson_Tatum',
            "chinese_name": "杰森·塔图姆",
            "stress": "7.63亿次",
            "extra": [datas.get('Jayson_Tatum'), hitrates.get('Jayson_Tatum')]
        },
        {
            "player_name": 'Kevin_Durant',
            "chinese_name": "凯文·杜兰特",
            "stress": "6.48亿次",
            "extra": [datas.get('Kevin_Durant'), hitrates.get('Kevin_Durant')]
        },
        {
            "player_name": 'Jimmy_Butler',
            "chinese_name": "吉米·巴特勒",
            "stress": "6.34亿次",
            "extra": [datas.get('Jimmy_Butler'), hitrates.get('Jimmy_Butler')]
        },
        {
            "player_name": 'Giannis_Antetokounmpo',
            "chinese_name": "扬尼斯·阿德托昆博",
            "stress": "5.92亿次",
            "extra": [datas.get('Giannis_Antetokounmpo'), hitrates.get('Giannis_Antetokounmpo')]
        },
        {
            "player_name": 'Jamal_Murray',
            "chinese_name": "贾马尔·穆雷",
            "stress": "4.56亿次",
            "extra": [datas.get('Jamal_Murray'), hitrates.get('Jamal_Murray')]
        },
        {
            "player_name": 'Anthony_Davis',
            "chinese_name": "安东尼·戴维斯",
            "stress": "4.56亿次",
            "extra": [datas.get('Anthony_Davis'), hitrates.get('Anthony_Davis')]
        },
        {
            "player_name": 'Kyrie_Irving',
            "chinese_name": "凯里·欧文",
            "stress": "4.54亿次",
            "extra": [datas.get('Kyrie_Irving'), hitrates.get('Kyrie_Irving')]
        },
        {
            "player_name": 'Austin_Reaves',
            "chinese_name": "奥斯汀·里夫斯",
            "stress": "4.10亿次",
            "extra": [datas.get('Austin_Reaves'), hitrates.get('Austin_Reaves')]
        },
        {
            "player_name": 'Joel_Embiid',
            "chinese_name": "乔尔·恩比德",
            "stress": "3.96亿次",
            "extra": [datas.get('Joel_Embiid'), hitrates.get('Joel_Embiid')]
        },
        {
            "player_name": 'Ja_Morant',
            "chinese_name": "贾·莫兰特",
            "stress": "3.85亿次",
            "extra": [datas.get('Ja_Morant'), hitrates.get('Ja_Morant')]
        },
    ]
    ImageUtils().long_img(list(reversed(players)), 'shemei')
