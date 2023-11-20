import os
from datetime import datetime

from nba.constants import nba_teams
from tools.image_utils import ImageUtils
from tools.nba_utils import NbaUtils
from tools.sqlUtils import get_sql

nba_utils = NbaUtils()
today = datetime.now().strftime("%Y-%m-%d")
file_path = "F:\\notebooks\\其他\\draft"


def game_data(games, tag):
    file_name = os.path.join(file_path, f"{today}_{tag}")
    sorted_games = sorted(games, key=lambda x: x['fg3'])
    with open(file_name, "w", encoding="utf-8") as file:
        i = len(sorted_games)
        for game in sorted_games:
            player_name = game.get('player_name').replace("'", "''")
            basic_info = nba_utils.get_basic_info(player_name)
            file.write(f"#### {i}：**{basic_info.get('chinese_name')}**\n\n")
            if not basic_info.get('draft_position'):
                file.write(f"选秀：**{basic_info.get('draft_year')}**年落选秀\n\n")
            elif basic_info.get('draft_position') == 1:
                file.write(f"选秀：**{basic_info.get('draft_year')}**年状元秀\n\n")
            elif basic_info.get('draft_position') == 2:
                file.write(f"选秀：**{basic_info.get('draft_year')}**年榜眼秀\n\n")
            elif basic_info.get('draft_position') == 3:
                file.write(f"选秀：**{basic_info.get('draft_year')}**年探花秀\n\n")
            else:
                file.write(
                    f"选秀：**{basic_info.get('draft_year')}**年第**{basic_info.get('draft_position')}**顺位\n\n")
            hit_rate = f"投篮{game.get('fg')}/{game.get('fga')}，三分球{game.get('fg3')}/{game.get('fg3a')}，罚球{game.get('ft')}/{game.get('fta')}"
            print(basic_info, hit_rate)
            ImageUtils().draw_text(basic_info.get('code'), game.get('team'), tag,
                                   hit_rate.replace("，", " | "), (
                                       '┏',
                                       '得分：', f"{game.get('pts')}",
                                       '篮板：', f"{game.get('reb')}",
                                       '助攻：', f"{game.get('ast')}",
                                       '抢断：', f"{game.get('stl')}",
                                       '盖帽：', f"{game.get('blk')}",
                                       '┛'), i)
            file.write(
                f"![{basic_info.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\dataimg\\{basic_info.get('code')}_{tag}_{i}.png)\n\n")
            win_or_loss = "战胜" if game.get('game_win') else "不敌"
            file.write(
                f"在{game.get('game_date')}，{nba_teams.get(game.get('team'))}{win_or_loss}{nba_teams.get(game.get('opp'))}的比赛中，{basic_info.get('chinese_name')}上场{str(game.get('playing_time'))[2:]}\n\n")
            file.write(
                f"贡献：**{game.get('pts')}分 | {game.get('reb')}篮板 | {game.get('ast')}助攻 | {game.get('stl')}抢断 | {game.get('blk')}盖帽**\n\n")
            file.write(f"投篮：{hit_rate}，三分球命中率达到{round(game.get('fg3') * 100 / game.get('fg3a'), 1)}%\n\n")

            i -= 1


if __name__ == '__main__':
    sql = """SELECT *
        FROM public.player_regular_gamelog
        WHERE fg3a > 0 -- To avoid division by zero
          AND (fg3::float / fg3a) >= 0.6
          AND fg3a >= 10 and season =2024;
        """
    games = get_sql(sql)
    game_data(games, '3pt')
