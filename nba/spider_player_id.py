import requests

from tools.sqlUtils import update_signal

for i in range(2021, 2023):
    s = int(str(i)[2:]) + 1
    season = f"{i}-{s}"
    print(season)
    url = f"https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=Totals&Scope=S&Season={season}&SeasonType=Regular%20Season&StatCategory=PTS"

    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Origin": "https://www.nba.com",
        "Referer": "https://www.nba.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()  # Assuming the response is in JSON format
        rows = data.get('resultSet').get('rowSet')
        for row in rows:
            player_name = row[2]
            player_id = row[0]
            print(f"name:{player_name},id:{player_id}")
            update_sql = f"""update public.player_draft set player_id = %s where player_name=%s;"""
            update_signal(update_sql, (player_id, player_name))

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
