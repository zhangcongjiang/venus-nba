from PIL import Image
import os

# 源文件夹路径和目标文件夹路径
source_folder = 'F:\\pycharm_workspace\\venus\\nba\\img'
target_folder = 'F:\\pycharm_workspace\\venus\\nba\\image'

# 获取源文件夹中的所有文件
file_list = os.listdir(source_folder)

# 遍历文件夹中的所有文件
for file_name in file_list:
    # 检查文件是否为图片文件（可以根据需要添加更多的图片格式）
    if file_name.lower().endswith(('.png')):
        # 源文件的完整路径
        source_path = os.path.join(source_folder, file_name)
        file_size = os.path.getsize(source_path)
        file_size_mb = file_size / 1024 / 1024
        print(f"{file_name}大小: {file_size_mb:.2f} MB")
        # 打开图片
        img = Image.open(source_path)

        # 修改图片尺寸，长度改为1200，宽度自适应
        new_width = 1200
        ratio = new_width / float(img.size[0])
        new_height = int(float(img.size[1]) * ratio)
        resized_img = img.resize((new_width, new_height))

        # 目标文件的完整路径
        target_path = os.path.join(target_folder, file_name)

        # 保存修改后的图片
        resized_img.save(target_path, quality=80)
        file_size = os.path.getsize(target_path)
        file_size_mb = file_size / 1024 / 1024
        print(f"修改后{file_name}大小: {file_size_mb:.2f} MB")
        print(f"图片 '{file_name}' 已经修改尺寸并保存到 '{target_path}'")

print("所有图片处理完成。")
