# -*- coding: utf-8 -*-
import textwrap

from PIL import Image, ImageDraw, ImageFont


def resize_img(img_path, new_width=720):
    img = Image.open(img_path)
    width, height = img.size
    new_height = int(height * new_width / width)
    img = img.resize((new_width, new_height), resample=Image.LANCZOS)
    return img


def signal_img(data_dict):
    date = data_dict.get("time")
    title = data_dict.get("title")
    pic_path = data_dict.get("img_path")
    pic_image = resize_img(pic_path)
    pic_height = pic_image.height

    font_path = 'simhei.ttf'
    font_size = 36
    title_font_size = 36
    title_spacing = 64
    spacing = 36
    font = ImageFont.truetype(font_path, font_size)
    title_font = ImageFont.truetype(font_path, title_font_size)
    # 标题行，每行最多12个字
    title_lines = textwrap.wrap(title, width=19)

    width = 760
    height = pic_height + title_spacing * (len(title_lines) + 1) + 2 * spacing
    image = Image.new('RGB', (width, height), 'white')

    # 在图片上添加文字
    draw = ImageDraw.Draw(image)
    # 上方留白
    y_position = spacing
    # 画时间
    draw.rounded_rectangle((-spacing, y_position, 460, spacing + title_spacing), spacing, width=2,
                           fill="#f34341")

    draw.text((30, spacing + (title_spacing - spacing) / 2), date, fill='white', font=font)

    # 画标题
    y_position = title_spacing + spacing
    i = 0
    regex = len(title_lines) * (title_spacing - title_font_size) / (len(title_lines) + 1)
    for line in title_lines:
        draw.text((40, regex + y_position + i * (regex + title_font_size)), line, fill='#484949', font=title_font)
        i += 1

    # 画正文
    y_position += len(title_lines) * title_spacing

    draw.rounded_rectangle((19, y_position - 1, 741, y_position + pic_height + 1), width=1, fill="#f34341")
    image.paste(pic_image, (20, y_position))

    y_position += pic_height

    for x in range(0, 760, 8):
        # 画底部虚线分隔
        draw.line([(0, y_position + spacing - 2), (x + 4, y_position + spacing - 2)], fill='#efefef',
                  width=2)

    return image


if __name__ == '__main__':
    data = [
        {
            "time": "保罗·班切罗（魔术）",
            "title": "上赛季最佳新秀获得者，目前已经是被征召进入美国国家队，即将代表美国参加在菲律宾举行的男篮世界杯，因此没有参加本届夏季联赛。",
            "img_path": "F:\\pycharm_workspace\\venus\\src\\background.png"
        },
        {
            "time": "沃克·凯斯勒（爵士）",
            "title": "与班切罗一样，凯斯勒也进入了美国国家队最终12人的大名单，将代表美国出战男篮世界杯，因此也没有参加本届夏季联赛。",
            "img_path": "F:\\pycharm_workspace\\venus\\src\\josh_okogie.png"
        },
        {
            "time": "杰伦·威廉姆斯（雷霆）",
            "title": "杰伦·威廉姆斯只参加了一场在盐湖城的夏季联赛，出战21分钟，14投8中，三分球5投3中，得到21分4篮板2助攻1盖帽，仅用一场比赛就展示了他的驾驭比赛的能力和得分能力高出其他人一档。他在新秀赛季就已经是联盟中最好的新秀之一，他在第二年看起来准备好了迎接更大的挑战。",
            "img_path": "F:\\pycharm_workspace\\venus\\src\\img_2.png"
        },
        {
            "time": "马图林（步行者）",
            "title":"马图林是新秀一阵中夏季联赛表现最一般的球员，两场比赛分别贡献17分和27分，命中率和场上影响力也十分一般，完美融入了这个分段。马图林上赛季常规赛也是高开低走，一度场均贡献超过20分，后来就撞到了新秀墙，赛季结束时得分下滑到了16.7，看样子新秀墙马图林还没有撞破。",
            "img_path": "F:\\pycharm_workspace\\venus\\src\\img_3.png"
        },
        {
            "time": "基根·穆雷（国王）",
            "title": "穆雷参加了两场夏季联赛，分别贡献29分和41分，两场比赛只有四个字可以来形容穆雷的实力，“降维打击”。上赛季他就是联盟中最好的新秀之一，他在西部三号种子的队伍中获得了宝贵的季后赛经验，下赛季我们将见证穆雷的成长。",
            "img_path": "F:\\pycharm_workspace\\venus\\src\\img_4.png"
        },
        {
            "time": "贾巴里·史密斯（火箭）",
            "title": "贾巴里·史密斯在夏季联赛中的表现可谓大开杀戒。第一场比赛就贡献技惊四座的0.6秒压哨绝杀，第二场又是狂砍38分教四年级的榜眼怀斯曼做人。两场比赛他平均每场得到35.5分，7个篮板，4次助攻和1次盖帽，投篮命中率达到48.8%。尽管他的三分球命中率不高，但他展示出了即使投篮不准也没人敢放的造威胁的能力，下个赛季探花秀必定乘风破浪，火箭的季后赛目标也更近一步。",
            "img_path": "F:\\pycharm_workspace\\venus\\src\\img_5.png"
        },
        {
            "time": "塔里·伊森（火箭）",
            "title": "塔里·伊森在2022年的选秀中被休斯顿火箭队选中，他立即就展现出了他的价值。他在拉斯维加斯的两场比赛中，他的身体素质在场上的两端都压倒了对手。他平均每场得到23分，9.5个篮板，4次助攻，3次盖帽和1次抢断，投篮命中率为48.7%。伊森的防守潜力是他最大的优点，但他的进攻也同样引人注目。他的球技和驾驭比赛的能力使他在火箭队的阵容中占据了一席之地，他和贾巴里·史密斯就是火箭未来锋线的答案。",
            "img_path": "F:\\pycharm_workspace\\venus\\src\\img_6.png"
        },
        {
            "time": "杰伦·杜伦（活塞）",
            "title": "杰伦·杜伦在2022年的选秀中被底特律活塞队选中，虽然年龄不大但他具有强壮的身体。在拉斯维加斯的两场比赛中，他展示了更高的技术水平，他以每场20分和9个篮板的成绩结束了他的比赛，投篮命中率高达68.2%。杜伦的力量和修长的臂展使他具有在篮下较强的得分能力，与队内四年级的榜眼怀斯曼相比，杜伦明显实力更强。",
            "img_path": "F:\\pycharm_workspace\\venus\\src\\img_7.png"
        },
        {
            "time": "杰登·艾维（活塞）",
            "title": "杰登·艾维在夏季联赛进攻效率方面略显不足，但他在活塞队的第二场比赛中表现出色，得到22分，10次助攻和2次抢断，投篮命中率为60%。他的速度和跳跃能力使他成为了联盟中最快的后卫之一，艾维有可能是下一个莫兰特。",
            "img_path": "F:\\pycharm_workspace\\venus\\src\\img_8.png"
        },
        {
            "time": "杰里米·索汉（马刺）",
            "title": "索汉是那种实用性的球员，粗糙中带着灵性，不以得分见长，在夏季联赛这种级别的比赛中没有太多用武之地，波波维奇也是发现了这一点，没有让索汉参加今年的下集联赛。",
            "img_path": "F:\\pycharm_workspace\\venus\\src\\img_9.png"
        }
    ]

    height = 200
    width = 800
    spacing = 46
    image = Image.new('RGB', (width, height), '#f54341')

    news_type = "夏季联赛"
    # 在图片上添加文字
    draw = ImageDraw.Draw(image)
    font_path = 'simhei.ttf'
    text1 = ' 二年级生降维打击'
    text2 = " 史密斯大开杀戒"
    font1 = ImageFont.truetype(font_path, 96)
    font2 = ImageFont.truetype(font_path, 48)
    font3 = ImageFont.truetype(font_path, 18)
    text_width1, text_height1 = draw.textsize(news_type, font=font1)  # 选择字体和字号
    text_width2, text_height2 = draw.textsize(text1, font=font2)
    text_x = (800 - text_width2 - text_width1) // 2  # 文字水平居中
    text_y = (200 - text_height1) // 2  # 文字垂直居中
    draw.text((text_x, text_y), news_type, font=font1, fill='#f8df29')
    draw.text((text_x + text_width1, text_y), text1, font=font2, fill='white')
    draw.text((text_x + text_width1, text_y + 48), text2, font=font2, fill='white')

    time_text = "开局一张图，故事全靠编"
    text_width, text_height = draw.textsize(time_text, font=font3)
    text_x = (800 - text_width) - 30  # 文字水平居中右
    text_y = 165  # 文字垂直居中
    draw.text((text_x, text_y), time_text, font=font3, fill='#bdbad1')

    summary1 = "  夏季联赛已经进入收官阶段，火箭上赛季探花贾巴里·史密斯和国王四号秀基根·穆雷在夏季联赛上都展示出了降维打击的实力，他俩上赛季分属最佳新秀阵容二阵和一阵，我们看下最佳新秀阵容的其他人表现如何。"
    summary2 = ""
    summary3 = ""
    summary_lines = textwrap.wrap(summary1, width=21)
    summary2_lines = textwrap.wrap(summary2, width=21)
    summary3_lines = textwrap.wrap(summary3, width=21)
    summary_lines.extend(summary2_lines)
    summary_lines.extend(summary3_lines)
    summay_font = ImageFont.truetype(font_path, 36)
    i = 0
    regex = len(summary_lines) * 10 / (len(summary_lines) + 1)

    image2 = Image.new('RGB', (width, len(summary_lines) * spacing), '#c8c8c8')
    draw2 = ImageDraw.Draw(image2)
    for line in summary_lines:
        draw2.text((20, regex + i * (regex + 36)), line, fill='#4e4e4e', font=summay_font)
        i += 1

    height += (len(summary_lines) + 1) * spacing
    imgs = []
    for item in data:
        img = signal_img(item)
        imgs.append((img, img.height))

        height += img.height

    merged_image = Image.new('RGB', (width, height), '#c8c8c8')
    # 将第一张图片粘贴在新图像的上方
    merged_image.paste(image, (0, 0))

    # 将第二张图片粘贴在新图像的下方
    merged_image.paste(image2, (0, 200))

    dpi = 200

    current_height = 200 + image2.height
    for item in imgs:
        merged_image.paste(item[0], (20, current_height))
        current_height += item[1]

    merged_image.show()

    image = merged_image.resize((int(width * dpi / 100), int(height * dpi / 100)), resample=Image.LANCZOS)
    image.save(f'F:\\pycharm_workspace\\venus\\img\\today\\{news_type}.jpg', dpi=(dpi, dpi))
