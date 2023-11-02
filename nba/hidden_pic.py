from PIL import Image, ImageDraw

# 打开要隐藏的图片和黑色背景图片
hidden_image = Image.open("img_2.png")
background = Image.new("RGB", hidden_image.size, "black")

# 创建一个混合图像
alpha = 0.3  # 调整alpha值以控制图像的透明度
mixed_image = Image.blend(background, hidden_image, alpha)

# 保存混合图像
mixed_image.save("harden.png")

# 显示混合图像
mixed_image.show()
