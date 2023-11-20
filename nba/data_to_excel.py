from collector.database import PsqlConnect
import pandas as pd

from nba.constants import nba_teams
from tools.sqlUtils import get_sql


def execute_sql(sql):
    psql = PsqlConnect()
    conn = psql.connect(host="localhost",
                        database="spider",
                        user="postgres",
                        password="postgres",
                        port="5432")

    cur = conn.cursor()

    cur.execute(sql)
    rows = cur.fetchall()

    # 定义一个空列表，用于存储转换后的字典
    result = []

    # 遍历查询结果，并将每一行转换为字典
    for row in rows:
        # 将查询结果的列名和对应的值组成键值对，并添加到字典中
        # row_dict = dict(zip([column[0] for column in cur.description], row))
        # 将字典添加到结果列表中
        result.append(row)

    cur.close()
    conn.close()

    return result


if __name__ == '__main__':
    players = get_sql(
        "select player_name,chinese_name,draft_position,team from public.player_draft where draft_year=2009 and attend =TRUE order by draft_position;")
    rows = []
    keys = []
    format_rows = []
    for player in players:
        sql = f"""SELECT EXTRACT(YEAR FROM game_date) AS year,
           EXTRACT(MONTH FROM game_date) AS month,
           SUM(pts) AS total_points
    FROM public.player_regular_gamelog
    WHERE player_name = '{player.get('player_name')}'
    GROUP BY EXTRACT(YEAR FROM game_date), EXTRACT(MONTH FROM game_date)
    ORDER BY year, month;"""
        result = execute_sql(sql)
        row = {
            "名称": f"{player.get('chinese_name')}({player.get('draft_position')})",
            "英文名": player.get('player_name'),
            "母队": nba_teams.get(player.get('team'))
        }
        sum = 0
        for data in result:
            month = f"{str(data[0]).split('.')[0]}-{str(data[1]).split('.')[0].zfill(2)}"
            if month not in keys:
                keys.append(month)
            row[month] = data[2]
        rows.append(row)

    for key in keys:
        for row in rows:
            if key not in row.keys():
                row[key] = 0

    sorted_keys = sorted(keys)
    for row in rows:
        score = 0
        format_row = {
            '名称': row['名称']
        }
        for key in sorted_keys:
            score += row[key]
            format_row[key] = score
        format_rows.append(format_row)

    df = pd.DataFrame(format_rows)
    df.to_excel('2009.xlsx', index=False)
