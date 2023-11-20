import os
from datetime import datetime

from tools.image_utils import ImageUtils
from tools.sqlUtils import get_sql

file_path = "F:\\notebooks\\其他\\draft"
today = datetime.now().strftime("%Y-%m-%d")

if __name__ == '__main__':

    tag = 'today_stars'
    file_name = os.path.join(file_path, f"{today}_{tag}.md")

    today_players = get_sql(
        "SELECT * FROM public.player_regular_gamelog where game_date =CURRENT_DATE ORDER BY (pts + reb + ast + stl + blk) DESC LIMIT 3;")
    with open(file_name, "w", encoding="utf-8") as file:
        i = 1
        imgs = []
        for player in today_players:
            player_draft = get_sql(
                f"""select * from public.player_draft where player_name = '{player.get("player_name")}';""")
            print(player_draft[0])

            file.write(f"{i}.{player_draft[0].get('chinese_name')}\n")
            imgs.append(player_draft[0].get('code'))

            hit_rate = f"投篮：{player.get('fg')}/{player.get('fga')} | 三分：{player.get('fg3')}/{player.get('fg3a')} | 罚球：{player.get('ft')}/{player.get('fta')} "
            data = {
                '得分：': player.get('pts'),
                '篮板：': player.get('reb'),
                '助攻：': player.get('ast'),
                '抢断：': player.get('stl'),
                '盖帽：': player.get('blk'),
                '失误：': player.get('tov')
            }
            pd_str = ImageUtils().format_draw_data(player_draft[0].get("code"), tag, hit_rate, data)
            file.write(f"数据：{pd_str}\n\n")
            file.write(f"命中率：{hit_rate}\n\n")

            file.write("---\n\n")
            i += 1
        for img in imgs:
            file.write(
                f"![{player_draft[0].get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{img}_{tag}.png)\n\n")
