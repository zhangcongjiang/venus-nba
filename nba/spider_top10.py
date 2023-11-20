# -*- coding: utf-8 -*-
from datetime import datetime

from tools.nba_utils import get_player_last_season_data
from tools.sqlUtils import get_sql

if __name__ == '__main__':
    sql = """select id, code,player_name,chinese_name,draft_year,team,draft_position from public.player_active  where draft_year<2009  order by draft_year desc,draft_position desc limit 20;"""
    players = get_sql(sql)

    today = datetime.now().strftime("%Y-%m-%d")
    file_name = f"F:\\notebooks\\其他\\draft\\{today}_top10.md"
    with open(file_name, "w", encoding="utf-8") as file:
        i = 20
        for p in players:
            print(p)
            i -= 1
            file.write(f"#### 第{i}位. **{p.get('chinese_name')}**\n\n")
            file.write(f"**{p.get('draft_year')}**年第**{p.get('draft_position')}**顺位进入联盟\n\n")
            last_season_data = get_player_last_season_data(p.get('player_name'))
            print({p.get('code')}, last_season_data)
            if not last_season_data:
                file.write(f"上赛季未出战任何比赛\n\n")
                file.write(
                    f"![{p.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\img\\{p.get('code')}.png)\n\n")
                continue

            file.write(f"年薪{last_season_data.get('salary')}\n\n")

            file.write(
                f"上赛季效力于**{last_season_data.get('team')}**，共出战{last_season_data.get('attend')}场比赛\n\n")
            file.write(f"{last_season_data.get('data').replace(' | ', ' ')}\n\n")
            # file.write(f"{last_season_data.get('hit_rate')}\n\n")
            file.write(
                f"![{p.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\img\\{p.get('code')}.png)\n\n")

            file.write("---\n\n")
