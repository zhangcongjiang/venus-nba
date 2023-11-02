import textwrap
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont


def resize_img(img_path, min_height, max_height, max_width=240):
    img = Image.open(img_path)
    width, height = img.size
    new_width = max_width
    new_height = int(height * (max_width / width))
    if new_height < min_height:
        new_width = int(new_width * new_height / min_height)
        new_height = min_height
    if new_height > max_height:
        new_width = int(new_width * new_height / min_height)
        new_height = max_height
    if new_width > max_width:
        new_width = max_width
    else:
        new_width = max_width
    img = img.resize((new_width, new_height), resample=Image.LANCZOS)
    return img


def signal_img(data_dict):
    date = data_dict.get("time")
    title = data_dict.get("title")
    msg = data_dict.get("msg")

    font_path = 'simhei.ttf'
    font_size = 26
    title_font_size = 36
    spacing = 36
    title_spacing = 64
    font = ImageFont.truetype(font_path, font_size)
    title_font = ImageFont.truetype(font_path, title_font_size)
    # 标题行，每行最多12个字
    title_lines = textwrap.wrap(title, width=12)
    # 信息行，每行最多17个字
    msg_lines = textwrap.wrap(msg, width=17)
    width = 760
    height = spacing * (len(msg_lines) + 3) + title_spacing * len(title_lines)
    image = Image.new('RGB', (width, height), 'white')

    # 在图片上添加文字
    draw = ImageDraw.Draw(image)
    # 上方留白
    y_position = spacing
    # 画时间
    draw.rounded_rectangle((-spacing, y_position, 260, spacing * 2), spacing, width=2, fill="#f34341")

    draw.text((30, spacing + 5), date, fill='white', font=font)

    # 画标题
    y_position = spacing * 2
    i = 0
    regex = len(title_lines) * (title_spacing - title_font_size) / (len(title_lines) + 1)
    for line in title_lines:
        draw.text((40, regex + y_position + i * (regex + title_font_size)), line, fill='#484949', font=title_font)
        i += 1

    # 画正文
    y_position = spacing * 2 + len(title_lines) * title_spacing
    draw.rounded_rectangle((20, y_position, 740, y_position + len(msg_lines) * spacing), spacing / 2,
                           width=2, fill="#efefef")
    i = 0
    for line in msg_lines:
        draw.text((40, 5 + y_position + i * spacing), line, fill='#484949', font=font)
        i += 1

    # 画图片，图片宽度240，最大高度标题高度+正文高度
    pic_path = data_dict.get("img_path")
    pic_image = resize_img(pic_path, min_height=len(msg_lines) * spacing + title_spacing,
                           max_height=len(msg_lines) * spacing + title_spacing * len(title_lines) + spacing)
    pic_height = pic_image.height
    pic_width = pic_image.width
    pic_y = spacing + int((len(title_lines) * title_spacing + len(msg_lines) * spacing - pic_height) / 2)
    draw.rounded_rectangle(
        (489 + int((240 - pic_width) / 2), pic_y - 1, 731 - int((240 - pic_width) / 2), pic_y + pic_height + 1),
        width=1,
        fill="#f34341")
    image.paste(pic_image, (490 + int((240 - pic_width) / 2), pic_y))

    y_position = spacing * 2 + len(title_lines) * title_spacing + len(msg_lines) * spacing
    for x in range(0, 760, 8):
        # 画底部虚线分隔
        draw.line([(0, y_position + spacing - 2), (x + 2, y_position + spacing - 2)], fill='#efefef', width=2)

    return image


if __name__ == '__main__':
    data = [
        {
            "time": "第一名 2016",
            "title": "贾玛尔-穆雷 掘金",
            "msg": "穆雷常规赛经常不温不火，季后赛大杀四方，虽然没有入选过全明星，不过今年作为绝对的外线核心帮助掘金夺得总冠军，穆雷已经进入生涯巅峰，未来几年，他与约基奇所率领的掘金都会是冠军的强力竞争选手，穆雷目前已经是顶薪球员，下赛季入选全明星板上钉钉，排名第一。",
            "img_path": "F:\\pycharm_workspace\\venus\\src\\2016-7.jpg"
        },
        {
            "time": "第二名 2014",
            "title": "朱利叶斯-兰德尔 湖人",
            "msg": "拿到过进步最快球员，入选过两次全明星，尼克斯内线核心，身体强壮，技术全面但效率低下，常规赛超神，季后赛超鬼的代表人物，同时与恩比德一道是大后锋的代表人物，尼克斯无法更进一步与兰德尔有很大的关系，但是两次入选全明星已是近十年7号秀中最多的了，排名第二。",
            "img_path": "F:\\pycharm_workspace\\venus\\src\\2014-7.jpg"
        },
        {
            "time": "第三名 2017",
            "title": "劳里-马尔卡宁 森林狼",
            "msg": "马尔卡宁上赛季完成进化，进攻无死角且极其高效，成功打进全明星并获得进步最快球员奖项，爵士明确表示将马尔卡宁作为建队基石，树挪死人挪活的典范。凭借全明星+MIP，第三名当之无愧。",
            "img_path": "F:\\pycharm_workspace\\venus\\src\\2017-7.jpg"
        },
        {
            "time": "第四名 2018",
            "title": "温德尔-卡特 公牛",
            "msg": "武切维奇的交易中被送到魔术，卡特是魔术雷打不动的主力前锋，不过随着班切罗和瓦格纳的崛起，卡特的未来可能不在魔术，卡特是一名合格的锋线轮换，但是离全明星还有很长的距离要走，排名第四。",
            "img_path": "F:\\pycharm_workspace\\venus\\src\\2018-7.png"
        },
        {
            "time": "第五名 2019",
            "title": "科比-怀特 公牛",
            "msg": "经常调侃上限乔丹普洱，下限科比怀特，怀特其实是一名合格的轮换球员，有着出色的三分球能力，打球风格类似于JR史密斯，休赛季以3年4000万美金的价格续约公牛，注定了将来只会是一名角色球员，目前排名第五。",
            "img_path": "F:\\pycharm_workspace\\venus\\src\\2019-7.jpg"
        },
        {
            "time": "第六名 2022",
            "title": "谢登-夏普 开拓者",
            "msg": "运动能力顶级，天赋满满，投射能力优秀，新秀赛季下半年开始展露锋芒，交易走利拉德后，夏普将得到大量的机会，前途一片光明，暂时排名第六，后续可能向上提升。",
            "img_path": "F:\\pycharm_workspace\\venus\\src\\2022-7.png"
        },
        {
            "time": "第七名 2021",
            "title": "乔纳森-库明加 勇士",
            "msg": "  身体素质极其优秀的足尺寸锋线，可惜库明加是需要有球在手的核心打法，在勇士这样一支争冠的球队里，库明加得不到足够的锻炼，好在即使已经三年级了，也才只有20岁，在勇士队内年轻人所剩无几的情况下，库明加未来还有无限可能，暂时排名第七。",
            "img_path": "F:\\pycharm_workspace\\venus\\src\\2021-7.jpg"
        },
        {
            "time": "第八名 2015",
            "title": "伊曼纽尔-穆迪埃 掘金",
            "msg": "穆迪埃曾是全美第一高中生，高中毕业后由于家庭贫困没有进入ncaa就读，而是来CBA广东宏远打了一个赛季，选秀大会时曾穿着印有五星红旗的外套，被称为中国男孩，进入NBA后也曾作为核心球员培养，打出过全美第一高中生的水准，可惜始终没有达到预期，加上连续受伤病困扰，逐渐沉沦，穆迪埃是没有做好职业规划的反面教材，只能排名第八。",
            "img_path": "F:\\pycharm_workspace\\venus\\src\\2015-7.png"
        },
        {
            "time": "第九名 2020",
            "title": "基利安-海耶斯 活塞",
            "msg": "  活塞已经有了大年状元CC，加上海耶斯进步速度缓慢，虽然防守和组织能力还行，但是进攻效率极其低下，海耶斯新秀合同到期后，可能直接变成底薪球员，目前排名第九。",
            "img_path": "F:\\pycharm_workspace\\venus\\src\\2020-7.jpg"
        },
        {
            "time": "第十名 2013",
            "title": "本-麦科勒莫 国王",
            "msg": "身体素质单薄的神射手，除了三分其他都不行，国王鱼腩期间毁掉的高顺位天才之一，上赛季效力于CBA山东队，表现不是很理想，排名倒数第一。",
            "img_path": "F:\\pycharm_workspace\\venus\\src\\2013-7.jpg"
        }
    ]
    height = 200
    width = 800
    spacing = 36
    image = Image.new('RGB', (width, height), '#f54341')

    news_type = "七号秀"
    # 在图片上添加文字
    draw = ImageDraw.Draw(image)
    font_path = 'simhei.ttf'
    text1 = '穆雷领衔，多人获MIP'
    text2 = "中国男孩令人惋惜"
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

    summary1 = "    盘点近十年7号秀，穆雷作为绝对核心率领掘金夺冠，兰德尔与马尔卡宁均获得MIP并入选全明星，夏普和库明加也值得期待，七号秀的成材率绝对合格。"
    summary2 = "    贾马尔-穆雷虽然从未入选过全明星，不过依然排名第一，中国男孩'穆迪埃'为家庭过早进入职业赛场令人惋惜，曾在火箭效力过的本-麦科勒莫排名倒数第一。"
    summary_lines = textwrap.wrap(summary1, width=29)
    summary2_lines = textwrap.wrap(summary2, width=29)
    summary_lines.extend(summary2_lines)
    summay_font = ImageFont.truetype(font_path, 26)
    i = 0
    regex = len(summary_lines) * (spacing - 26) / (len(summary_lines) + 1)
    image2 = Image.new('RGB', (width, len(summary_lines) * spacing), '#c8c8c8')
    draw2 = ImageDraw.Draw(image2)
    for line in summary_lines:
        draw2.text((20, regex + i * (regex + 26)), line, fill='#4e4e4e', font=summay_font)
        i += 1
    height += len(summary_lines) * spacing

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

    dpi = 300

    current_height = 200 + image2.height
    for item in imgs:
        merged_image.paste(item[0], (20, current_height))
        current_height += item[1]

    merged_image.show()

    image = merged_image.resize((int(width * dpi / 100), int(height * dpi / 100)), resample=Image.LANCZOS)

    name = datetime.now().date()
    image.save(f'F:\\pycharm_workspace\\venus\\img\\today\\{name}.png', dpi=(dpi, dpi))
