from PIL import Image, ImageDraw

# 打开要隐藏的图片和黑色背景图片
hidden_image = Image.open("../nba/bkg.png")
resized_img = hidden_image.resize((1400, 1000))
background = Image.new("RGB", resized_img.size, "black")

# 创建一个混合图像
alpha = 0.3  # 调整alpha值以控制图像的透明度
mixed_image = Image.blend(background, resized_img, alpha)

# 保存混合图像
mixed_image.save("bkg2.png")
