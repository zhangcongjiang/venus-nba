import textwrap
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

from collector.data_collector import PsqlCollector


class TodayNews:
    @staticmethod
    def generator(news_type, datas):
        # 加载字体
        font_path = 'simhei.ttf'
        font_size = 24

        image = Image.new('RGB', (800, 200), '#e74032')

        # 在图片上添加文字
        draw = ImageDraw.Draw(image)

        text = f'新鲜事，一个不错过'
        font1 = ImageFont.truetype(font_path, 96)
        font2 = ImageFont.truetype(font_path, 48)
        text_width1, text_height1 = draw.textsize(news_type, font=font1)  # 选择字体和字号
        text_width2, text_height2 = draw.textsize(text, font=font2)
        text_x = (800 - text_width2 - text_width1) // 2  # 文字水平居中
        text_y = (200 - text_height1) // 2  # 文字垂直居中
        draw.text((text_x, text_y), news_type, font=font1, fill='#f8df29')
        draw.text((text_x + text_width1, (200 - text_height2) // 2), text, font=font2, fill='white')

        # 保存图片

        image1 = image
        font = ImageFont.truetype(font_path, font_size)
        draw1 = ImageDraw.Draw(image1)
        if len(datas) > 0:
            time_text = f"{len(datas)}条热点数据；时间：{datas[0].get('created_at').date()} "
            text_width, text_height = draw1.textsize(time_text, font=font)
            text_x = (800 - text_width) - 50  # 文字水平居中右
            text_y = 165  # 文字垂直居中
            draw1.text((text_x, text_y), time_text, font=font, fill='white')

        width = 800
        height = 40
        # 时间轴的位置
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
        return image1, image


if __name__ == '__main__':
    pc = PsqlCollector()
    datas = pc.today()
    split_dict = {}
    for data in datas:
        field_value = data.get('news_type')
        if field_value not in split_dict:
            split_dict[field_value] = []
        split_dict[field_value].append(data)
    for key in split_dict.keys():
        tn = TodayNews()
        image1, image2 = tn.generator(key, split_dict.get(key))

        dpi = 300
        width = 800
        height = image2.height + 200
        image = Image.new('RGB', (width, height))
        image.paste(image1, (0, 0))
        image.paste(image2, (0, 200))

        draw = ImageDraw.Draw(image)
        line_start = (0, 200)
        line_end = (800, 200)
        draw.line([line_start, line_end], fill='red', width=2)

        image = image.resize((int(width * dpi / 100), int(height * dpi / 100)), resample=Image.LANCZOS)

        name = datetime.now().date()
        image.save(f'F:\\pycharm_workspace\\venus\\img\\today\\{key}_{name}.png', dpi=(dpi, dpi))
