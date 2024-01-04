import os.path

import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table

table_path = "F:\\pycharm_workspace\\venus\\nba\\game_tables"


def highlight_rows(s):
    return ['background-color: #40466e; color: white; font-weight: bold' if i < 5 else '' for i, _ in enumerate(s)]


# 读取CSV文件
def draw_table(file_path, game_id, tag):
    df = pd.read_csv(file_path, encoding='utf-8')

    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文显示
    plt.rcParams['axes.unicode_minus'] = False

    # 创建图表
    fig, ax = plt.subplots(figsize=(16, 16), dpi=300)

    # 移除坐标轴
    ax.axis('off')

    # 绘制表格
    tbl = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center', bbox=[0, 0, 1, 1])

    # 设置单元格宽度自适应
    tbl.auto_set_column_width([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    tbl.set_fontsize(32)

    # 设置颜色
    for i, key in enumerate(tbl.get_celld().keys()):
        cell = tbl.get_celld()[key]
        if key[0] == 0:
            cell.set_fontsize(24)
            cell.set_text_props(weight='bold')
            cell.set_facecolor('#40466e')  # 设置标题行背景色
            cell.set_text_props(color='white')  # 设置标题行文字颜色
        elif key[0] < 6:
            cell.set_facecolor('lightyellow')  # 设置前五行的背景色
        else:
            cell.set_facecolor('#f4f4f4')  # 设置后面行的背景色

    # 调整布局
    plt.tight_layout()

    # 保存图表
    img_path = os.path.join(table_path, f'{game_id}_{tag}.png')
    plt.savefig(img_path, bbox_inches='tight', pad_inches=0.05)


if __name__ == '__main__':
    draw_table("F:\\pycharm_workspace\\venus\\nba\\csv\\0022300421_away.csv", 1, 1)
