import re

from tools.sqlUtils import get_sql, update_signal

players = get_sql("select player_name from public.player_active where href ='';")

for player in players:
    with open('player.txt', 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, start=1):
            # 在当前行中搜索指定内容
            if re.search(player.get('player_name'), line):
                code = line.strip().split(',')[0]
                href = f"/players/{code[0]}/{code}.html"
                update_sql = f"""update public.player_active set href = %s where player_name=%s;"""
                update_signal(update_sql, (href, player.get('player_name')))
                # 如果找到匹配的行，则打印行号和行内容
                print(f"{player}  {line.strip().split(',')[0]}")
