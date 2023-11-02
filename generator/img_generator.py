import textwrap

from PIL import Image, ImageDraw, ImageFont

from collector.data_collector import PsqlCollector


class ImgGenerator:

    @staticmethod
    def generator(source, datas):
        # 加载字体
        font_path = 'simhei.ttf'
        font_size = 24
        font = ImageFont.truetype(font_path, font_size)

        # image1 = Image.open(f'../src/{source}.png')
        # draw1 = ImageDraw.Draw(image1)
        # if len(datas) > 0:
        #     time_text = f"{len(datas)}条数据；时间：{datas[0].get('created_at').date()} {datas[0].get('created_at').hour}时 ~ {datas[-1].get('created_at').date()} {datas[-1].get('created_at').hour}时"
        #     text_width, text_height = draw1.textsize(time_text, font=font)
        #     text_x = (800 - text_width) - 50  # 文字水平居中右
        #     text_y = 165  # 文字垂直居中
        #     draw1.text((text_x, text_y), time_text, font=font, fill='white')
        #
        width = 800
        height = 40
        # # 时间轴的位置
        center_x = 150
        for item in datas:
            text = f"{item.get('author')}: {item.get('msg')}"
            lines = textwrap.wrap(text, width=24)
            height += (len(lines) + 1) * 40

        # 创建空白图像
        image = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(image)

        # 画竖线
        draw.line((center_x, 0, center_x, height), fill='red', width=1)

        # 定义圆圈的半径和间距
        radius = 3

        spacing = 40
        i = 0
        front_date = None
        for data in datas:
            center_y = 40 + (i * spacing)
            date_time = data.get("created_at")
            date = date_time.date()
            if not front_date:
                front_date = date

            if date != front_date:
                for x in range(center_x, width, 6):
                    # 画虚线
                    draw.line([(x, center_y - 40), (x + 2, center_y - 40)], fill='red', width=1)
                front_date = date

            time = ":".join(
                [str(date_time.hour).zfill(2), str(date_time.minute).zfill(2), str(date_time.second).zfill(2)])

            draw.text((10, 16 + (i * spacing)), str(date), fill='red', font=font)
            draw.text((10, 40 + (i * spacing)), str(time), fill='red', font=font)
            draw.ellipse([(center_x - radius, center_y - radius), (center_x + radius, center_y + radius)],
                         fill='purple')
            lines = textwrap.wrap(f"{data.get('author')}: {data.get('msg')}", width=24)  # 设置每行的宽度
            # 在圆圈后面写文字
            for line in lines:
                draw.text((center_x + 10 + (radius * 2), 30 + (i * spacing)), line, fill='purple', font=font)
                i += 1
            i += 1
        return image


if __name__ == '__main__':
    key_words = ['华为']
    news = ['百度', '今日头条', '微博']
    ents = ['哔哩哔哩', '抖音']
    tech = ['36氪', 'Readhub', ]
    sources = {"hot_news": news,
               "hot_ent": ents,
               "hot_tech": tech}

    imgs = []
    dpi = 300
    width = 800
    total_height = 0
    for key in sources.keys():
        for item in sources.get(key):
            pc = PsqlCollector()
            data = pc.collect(key_words, item, key)
            print(data)
            ig = ImgGenerator()
            image2 = ig.generator(item, data)
            imgs.append(image2)
            total_height += image2.height
            #
            # height = image2.height + 200
            # image = Image.new('RGB', (width, height))
            # image.paste(image1, (0, 0))
            # image.paste(image2, (0, 200))
            #
            # draw = ImageDraw.Draw(image)
            # line_start = (0, 200)
            # line_end = (800, 200)
            # draw.line([line_start, line_end], fill='red', width=2)
            #
            # image = image.resize((int(width * dpi / 100), int(height * dpi / 100)), resample=Image.LANCZOS)
            #
            # name = "_".join(key_words)
            # image.save(f'F:\\pycharm_workspace\\venus\\img\\{item}_{name}.png', dpi=(dpi, dpi))

    total_image = Image.new('RGB', (width, total_height))
    current_height = 0
    for img in imgs:
        total_image.paste(img, (0, current_height))
        current_height += img.height

    draw = ImageDraw.Draw(total_image)
    line_start = (0, 200)
    line_end = (800, 200)

    image = total_image.resize((int(width * dpi / 100), int(total_height * dpi / 100)), resample=Image.LANCZOS)

    name = "_".join(key_words)
    image.save(f'F:\\pycharm_workspace\\venus\\img\\total_{name}.png', dpi=(dpi, dpi))
