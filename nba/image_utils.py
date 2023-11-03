import os

from PIL import Image, ImageDraw, ImageFont

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

    def draw_text(self, img_name, tag, hit_rate, data):
        font_path = 'simhei.ttf'
        img_path = os.path.join(SRC_PATH, img_name)
        img = Image.open(f"{img_path}.png")
        width, height = img.size
        spacing = int((height - 100) / len(data))
        font_size = spacing - 20
        if font_size > 42:
            font_size = 42
            spacing = 64
        font = ImageFont.truetype(font_path, font_size)

        # 在图片上添加文字
        draw = ImageDraw.Draw(img)
        i = 0
        for txt in data:
            if i == 0:
                x = 1000
            elif i == len(data) - 1:
                x = 1160
            else:
                x = 1060
            if i % 2 == 0:
                fill = '#ffffff'
            else:
                fill = '#eebe01'
            if i in [0, len(data) - 1]:
                fill = '#ffffff'
            draw.text((x, i * spacing), text=txt, font=font, fill=fill)
            i += 1
        hit_rate_font = ImageFont.truetype(font_path, 28)
        hit_rate_x = 1150 - len(hit_rate.split("|")) * 150
        draw.text((hit_rate_x, height - 50), text=hit_rate, font=hit_rate_font, fill='#eebe01')
        file = os.path.join(DST_PATH, img_name)
        img.save(f"{file}_{tag}.png")

    def format_draw_data(self, name, tag, hit_rate, data):
        pd_list = ['┏']
        pd = []
        for key, value in data.items():
            if value != 0:
                pd_list.append(key)
                pd_list.append(f"{value}")
                pd.append(f'{value}{key}')
        pd_str = " | ".join(pd).replace("得", "").replace("：", "")
        pd_list.append('┛')
        self.draw_text(name, tag, hit_rate, tuple(pd_list))
        return pd_str


if __name__ == '__main__':
    ImageUtils().draw_text('jabari_smith',
                           '投篮：100% ',
                           ('┏', '得分：', '25', '篮板：', '12.7', '┛'))
