import shutil

from PIL import Image
import os
import concurrent.futures

# 源文件夹路径和目标文件夹路径
source_folder = 'F:\\pycharm_workspace\\venus\\nba\\img'
target_folder = 'F:\\pycharm_workspace\\venus\\nba\\image'
logo_folder = 'F:\\pycharm_workspace\\venus\\nba\\logo'


def split_list(lst, num_parts):
    avg = len(lst) // num_parts
    remainder = len(lst) % num_parts
    result = []
    start = 0
    for i in range(num_parts):
        end = start + avg + (1 if i < remainder else 0)
        result.append(lst[start:end])
        start = end
    return result


def resize_img():
    # 获取源文件夹中的所有文件
    src_files = os.listdir(source_folder)
    dst_files = os.listdir(target_folder)
    del_files = [x for x in dst_files if x not in src_files]
    for item in del_files:
        os.remove(os.path.join(target_folder, item))
        print("删除", item)
    files = [x for x in src_files if x not in dst_files]
    split_files = split_list(files, 10)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 提交10个任务给线程池
        futures = [executor.submit(resize_img_task, file_list) for file_list in split_files]

        # 等待所有任务完成
        concurrent.futures.wait(futures)


def resize_img_task(file_list):
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
            target_path = os.path.join(target_folder, file_name.replace("'", ""))

            # 保存修改后的图片
            resized_img.save(target_path, quality=85)
            file_size = os.path.getsize(target_path)
            file_size_mb = file_size / 1024 / 1024
            print(f"修改后{file_name}大小: {file_size_mb:.2f} MB")
            print(f"图片 '{file_name}' 已经修改尺寸并保存到 '{target_path}'")

    print("所有图片处理完成。")


def clear_img():
    file_list = os.listdir(source_folder)

    # 遍历文件夹中的所有文件
    for file_name in file_list:
        # 检查文件是否为图片文件（可以根据需要添加更多的图片格式）
        if len(file_name.split("_")) > 3:
            source_path = os.path.join(source_folder, file_name)
            os.remove(source_path)
            print("清理图片：", file_name)


def rename_log_img():
    src_files = os.listdir(logo_folder)
    for item in src_files:
        if '-' in item:
            print(item)
            src = os.path.join(logo_folder, item)
            dst = os.path.join(logo_folder, item.replace("-", "_"))
            shutil.copy2(src, dst)


if __name__ == '__main__':
    resize_img()
