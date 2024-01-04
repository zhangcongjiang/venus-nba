from PIL import Image, ImageDraw, ImageFont

# 打开图片
img = Image.open('./logo/Bam_Adebayo_body.png')

# 获取图片的尺寸
width, height = img.size

# 创建新的图片，尺寸为440*700，背景色与原图一致
new_img = Image.new('RGBA', (width + 200, height + 300), (0, 0, 0, 0))

# 创建Draw对象，用于绘制文字和矩形框
draw = ImageDraw.Draw(new_img)

# 定义字体和文字大小，你需要替换为适合你的字体和大小
font = ImageFont.truetype('simhei.ttf', 36)

# 在图片上方添加矩形框，起始位置为(0, 0)，尺寸为440*100
draw.rectangle([0, 0, 440, 150], fill=(0, 0, 0))

# 在图片下方添加矩形框，起始位置为(0, height-100)，尺寸为440*100
draw.rectangle([0, height + 150, 440, height + 300], fill=(0, 0, 0))
draw.rectangle([440, 150, 640, height + 150], fill=(0, 0, 0,0))

# 计算文字宽度
text = "示例文字"
mask = font.getmask(text)
text_width = mask.size[0]

# 在上方矩形框中添加文字，起始位置为(220 - text_width/2, 25)，字体为前面定义的字体
draw.text((220 - text_width / 2, 30), "示例文字", font=font, fill=(255, 255, 255))

# 在下方矩形框中添加文字，起始位置为(220 - text_width/2, height-75)，字体为前面定义的字体
draw.text((220 - text_width / 2, height + 230), "示例文字", font=font, fill=(255, 255, 255))

new_img.paste(img, (0, 150))
# 保存新图片

# 在图片外围绘制白色outline
border_color = (255, 255, 255, 255)  # 红色outline的RGBA颜色值

# 上边框
draw.line([(0, 0), (width - 1, 0)], fill=border_color, width=2)
# 下边框
draw.line([(0, height + 298), (width - 1, height + 298)], fill=border_color, width=2)
# 左边框
draw.line([(0, 0), (0, height + 298)], fill=border_color, width=2)
# 右边框
draw.line([(width - 1, 0), (width - 1, height + 298)], fill=border_color, width=2)
new_img.save('output.png')
