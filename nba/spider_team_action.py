# -*- coding: utf-8 -*-
from datetime import datetime

from tools.nba_utils import get_game_log_with_team, handle_game

if __name__ == '__main__':
    games, ave = get_game_log_with_team('James Harden', 'PHI')

    today = datetime.now().strftime("%Y-%m-%d")
    file_name = f"F:\\notebooks\\其他\\draft\\{today}_team_action.md"

    with open(file_name, "w", encoding="utf-8") as file:
        file.write(f"詹姆斯·哈登为费城共出战{ave.get('attend')}场比赛。\n\n")
        file.write(
            f"场均可以贡献{ave.get('pts')}分{ave.get('rebs')}篮板{ave.get('asts')}助攻{ave.get('blks')}盖帽{ave.get('stls')}抢断\n\n")
        i = 1
        for game in games.values():
            p = handle_game(game)

            file.write(f"#### 第{i}位\n\n")

            file.write(f"比赛日期：{p.get('game_date')} 对阵 {p.get('opp')}\n\n")
            file.write(f"上场时间：{p.get('attend')}\n\n")
            file.write(f"数据：{p.get('data')}\n\n")
            file.write(f"命中率：{p.get('hit_rate')}\n\n")
            file.write(
                f"![{p.get('chinese_name')}](F:\\pycharm_workspace\\venus\\nba\\img\\james_harden.png)\n\n")

            file.write("---\n\n")
            i += 1
