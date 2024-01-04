from datetime import datetime, timedelta

from tools.sqlUtils import get_sql


class NbaUtils:
    def get_player_last_season_data(self, player_name):
        """
        查询上赛季表现
        :param player_name:
        :return:
        """
        sql = f"""SELECT player_name,team,game_attend, minutes_attend, pts, reb,  ast, fga, fg, fg3a, fg3, fta, ft, stl, blk, tov, salary
                                FROM public.player_regular_total_season where player_name='{player_name}' and season='2022-23';
                            """
        player_data = get_sql(sql)
        if not player_data:
            return {'last_score': 0,
                    'last_data': (0, 0, 0, 0, 0)}

        hit_rate = ''
        if player_data[0].get('fga'):
            hit_rate += f"投篮{round(player_data[0].get('fg') / player_data[0].get('fga') * 100, 1)}%，"
        if player_data[0].get('fg3a'):
            hit_rate += f"三分{round(player_data[0].get('fg3') / player_data[0].get('fg3a') * 100, 1)}%，"
        if player_data[0].get('fta'):
            hit_rate += f"罚球{round(player_data[0].get('ft') / player_data[0].get('fta') * 100, 1)}%"

        attend = player_data[0].get('game_attend')
        data_detail = (
            round(player_data[0].get('pts') / attend, 1), round(player_data[0].get('reb') / attend, 1),
            round(player_data[0].get('ast') / attend, 1), round(player_data[0].get('stl') / attend, 1),
            round(player_data[0].get('blk') / attend, 1))
        salary = f"{int(player_data[0].get('salary') / 10000)}万美金" if player_data[0].get('salary') else "暂无数据"
        team = player_data[0].get('team')

        return {
            'last_attend': attend,
            'last_data': data_detail,
            'last_hit_rate': (
                player_data[0].get('fg'), player_data[0].get('fga'),
                player_data[0].get('fg3'), player_data[0].get('fg3a'),
                player_data[0].get('ft'), player_data[0].get('fta')),
            'last_salary': salary,
            'last_team': team,
            'last_score': round(
                (player_data[0].get('pts') + player_data[0].get('reb') + player_data[0].get('ast') +
                 player_data[0].get('stl') + player_data[0].get('blk')) / attend, 1)
        }

    def last_week_data(self, player_name):
        sql = f"""SELECT * FROM player_regular_gamelog WHERE player_name = '{player_name}' and up=True AND game_date >= current_date - interval '7 days';"""
        games = get_sql(sql)
        total_win = total_loss = total_pts = total_rebs = total_asts = total_stls = total_tovs = total_blks = total_fg = total_fg3 = total_ft = 0
        total_fga = total_fg3a = total_fta = 1
        average_minutes, average_seconds = 0, 0
        win_opp = []
        loss_opp = []
        list_time = []
        game_data = (0, 0, 0, 0, 0, 0)
        for game in games:
            total_pts += game.get('pts')
            total_rebs += game.get('reb')
            total_asts += game.get('ast')
            total_stls += game.get('stl')
            total_blks += game.get('blk')
            total_tovs += game.get('tov')
            total_ft += game.get('ft')
            total_fta += game.get('fta')
            total_fg += game.get('fg')
            total_fga += game.get('fga')
            total_fg3 += game.get('fg3')
            total_fg3a += game.get('fg3a')
            list_time.append(game.get('playing_time'))

            if game.get('game_win'):
                total_win += 1
                win_opp.append(game.get('opp'))
            else:
                total_loss += 1
                loss_opp.append(game.get('opp'))
        total_time = sum(list_time, timedelta())
        if len(games):
            # 计算平均值
            average_time = total_time / len(list_time)
            average_minutes, average_seconds = divmod(average_time.seconds, 60)
            game_data = (
                round(total_pts / len(games), 1), round(total_rebs / len(games), 1), round(total_asts / len(games), 1),
                round(total_stls / len(games), 1), round(total_blks / len(games), 1), round(total_tovs / len(games), 1))
        return {
            'game_data': game_data,
            'game_attend': len(games),
            'game_hit_rate': (total_fg, total_fga, total_fg3, total_fg3a, total_ft, total_fta),
            'game_time': f"{average_minutes}:{str(average_seconds).zfill(2)}",
            'game_win': total_win,
            'win_opp': win_opp,
            'loss_opp': loss_opp,
            'game_score': (total_pts + total_rebs + total_asts + total_stls + total_blks),
            'game_loss': total_loss
        }

    def get_game_data(self, sql):
        games = get_sql(sql)
        hit_rate = ''
        total_win = total_loss = total_pts = total_rebs = total_asts = total_stls = total_tovs = total_blks = total_fg = total_fg3 = total_ft = 0
        total_fga = total_fg3a = total_fta = 1
        list_time = []
        if not len(games):
            return {
                'game_data': [0, 0, 0, 0, 0, 0],
                'game_fg': (0, 1),
                'game_fg3': (0, 1),
                'game_ft': (0, 1),
                'game_hit_rate': '',
                'game_time': 0,
                'game_win': 0,
                'game_attend': 0,
                'game_score': 0,
                'game_loss': 0
            }
        team = ''
        for game in games:
            total_pts += game.get('pts')
            total_rebs += game.get('reb')
            total_asts += game.get('ast')
            total_stls += game.get('stl')
            total_blks += game.get('blk')
            total_tovs += game.get('tov')
            total_ft += game.get('ft')
            total_fta += game.get('fta')
            total_fg += game.get('fg')
            total_fga += game.get('fga')
            total_fg3 += game.get('fg3')
            total_fg3a += game.get('fg3a')
            team = game.get('team')
            list_time.append(game.get('playing_time'))

            if game.get('game_win'):
                total_win += 1
            else:
                total_loss += 1

        total_time = sum(list_time, timedelta())
        # 计算平均值
        average_time = total_time / len(list_time)
        average_minutes, average_seconds = divmod(average_time.seconds, 60)
        if total_fga:
            hit_rate += f"投篮{round(total_fg / total_fga * 100, 1)}%，"
        if total_fg3a:
            hit_rate += f"三分{round(total_fg3 / total_fg3a * 100, 1)}%，"
        if total_fta:
            hit_rate += f"罚球{round(total_ft / total_fta * 100, 1)}%"
        ave = {
            'game_data': [
                round(total_pts / len(games), 1),
                round(total_rebs / len(games), 1),
                round(total_asts / len(games), 1),
                round(total_stls / len(games), 1),
                round(total_blks / len(games), 1),
                round(total_tovs / len(games), 1),
            ],
            'game_team': team,
            'game_fg': (total_fg, total_fga),
            'game_fg3': (total_fg3, total_fg3a),
            'game_ft': (total_ft, total_fta),
            'game_attend': len(games),
            'game_hit_rate': hit_rate,
            'game_time': f"{average_minutes}:{str(average_seconds).zfill(2)}",
            'game_win': total_win,
            'game_score': round(
                (total_pts + total_rebs + total_asts + total_stls + total_blks) / (
                    len(games)), 1),
            'game_loss': total_loss
        }

        return ave

    def best_game(self, player_name):
        sql = f"""SELECT *  
                FROM player_regular_gamelog  
                WHERE player_name = '{player_name}' and game_date between '2023-11-30' and '2023-12-31' and up=TRUE  
                ORDER BY (pts + reb + ast + stl + blk) DESC  
                LIMIT 1;"""
        result = get_sql(sql)
        if result:
            return result[0]
        else:
            return {}

    def career_data(self, player_name):
        sql = f"""SELECT
                player_name,
                SUM(pts) AS total_points,
                SUM(reb) AS total_rebounds,
                SUM(ast) AS total_assists,
                SUM(blk) AS total_blocks,
                SUM(stl) AS total_steals,
                SUM(tov) AS total_tovs,
                SUM(fg) AS total_fg,
                SUM(fga) AS total_fga,
                SUM(fg3a) AS total_fg3a,
                SUM(fg3) AS total_fg3,
                SUM(ft) AS total_ft,
                SUM(fta) AS total_fta,
                COUNT(*) AS total_games,
                COUNT(*) FILTER (WHERE game_win = True) AS total_win,
                COUNT(*) FILTER (WHERE game_win = False) AS total_loss,
                ARRAY_AGG(DISTINCT team) AS teams_played_for
            FROM
                public.player_regular_gamelog
            WHERE
                player_name = '{player_name}' and up=true
            GROUP BY
                player_name;
            """
        result = get_sql(sql)
        if not len(result):
            return {
                'hit_rate': (0, 1, 0, 1, 0, 1),
                'data': (0, 0, 0, 0, 0, 0),
                'total_win': 0,
                'total_loss': 0,
                'total_games': 0
            }
        hit_rate = (
            result[0].get('total_fg'), result[0].get('total_fga'),
            result[0].get('total_fg3'), result[0].get('total_fg3a') if result[0].get('total_fg3a') else 1,
            result[0].get('total_ft'), result[0].get('total_fta'))
        data = (result[0].get('total_points'),
                result[0].get('total_rebounds'),
                result[0].get('total_assists'),
                result[0].get('total_steals'),
                result[0].get('total_blocks'),
                result[0].get('total_tovs')
                )
        ave_data = {
            'hit_rate': hit_rate,
            'data': data
        }
        ave_data.update(result[0])
        return ave_data

    def get_game_log_with_team(self, player, team):
        """
        查询在某支球队期间的最佳表现
        :param player:
        :param team:
        :return:
        """
        sql = f"""SELECT id, player_name, season, game_date, up, playing_time, pts, reb, oreb, dreb, ast, fga, fg, fg3a, fg3, fta, ft, stl, blk, tov, plus_minus, team, opp, game_win FROM public.player_regular_gamelog where player_name ='{player}' and up=True and team = '{team}' order by  game_date;
                                """
        games = get_sql(sql)
        max_pts = max_rebs = max_asts = max_stls = max_blks = 0
        total_pts = total_rebs = total_asts = total_stls = total_blks = total_tovs = 0
        max_games = {}
        for game in games:
            total_pts += game.get('pts')
            total_rebs += game.get('reb')
            total_asts += game.get('ast')
            total_stls += game.get('stl')
            total_blks += game.get('blk')
            total_tovs += game.get('tov')
            if game.get('pts') >= max_pts:
                max_pts = game.get('pts')
                max_games['max_pts'] = game
            if game.get('reb') >= max_rebs:
                max_rebs = game.get('reb')
                max_games['max_rebs'] = game
            if game.get('ast') >= max_asts:
                max_asts = game.get('ast')
                max_games['max_asts'] = game
            if game.get('stl') >= max_stls:
                max_stls = game.get('stl')
                max_games['max_stls'] = game
            if game.get('blk') >= max_blks:
                max_blks = game.get('blk')
                max_games['max_blks'] = game
        ave = {
            'attend': len(games),
            'pts': round(total_pts / len(games), 1),
            'rebs': round(total_rebs / len(games), 1),
            'asts': round(total_asts / len(games), 1),
            'stls': round(total_stls / len(games), 1),
            'blks': round(total_blks / len(games), 1),
            'tovs': round(total_tovs / len(games), 1)
        }

        return max_games, ave

    def handle_game(self, game):
        attend = str(game.get('playing_time'))[2:]
        game_date = game.get('game_date')
        sum = game.get('pts') + game.get('reb') + game.get('ast') + game.get(
            'stl') + game.get('blk')
        data_detail = f"**{game.get('pts')}分 | {game.get('reb')}篮板 | {game.get('ast')}助攻 | {game.get('stl')}抢断 | {game.get('blk')}盖帽**"
        hit_rate = f"投篮{game.get('fg')}/{game.get('fga')}，三分球{game.get('fg3')}/{game.get('fg3a')}，罚球{game.get('ft')}/{game.get('fta')}"
        team = game.get('team')
        return {
            'attend': attend,
            'data': data_detail,
            'hit_rate': hit_rate,
            'game_date': game_date,
            'team': team,
            'sum': sum,
            'opp': game.get('opp'),
            'result': game.get('game_win')
        }

    def get_basic_info(self, player_name):
        sql = f"""select * from public.player_draft where player_name='{player_name}';"""
        basic_info = get_sql(sql)
        if not basic_info:
            basic_info = get_sql(f"""select * from public.player_active where player_name='{player_name}';""")
        basic_info = basic_info[0]

        draft_team = basic_info.get('team')
        return {
            'code': basic_info.get('code').replace("'", ""),
            'player_name': basic_info.get('player_name'),
            'chinese_name': basic_info.get('chinese_name'),
            'draft_year': basic_info.get('draft_year'),
            'draft_position': basic_info.get('draft_position'),
            'draft_team': draft_team,
            'birthday': basic_info.get('birthday'),
            'retirement': basic_info.get('retirement')
        }

    def get_game_log_with_season(self, player, season):
        """
        查询本赛季表现
        :param player:
        :param season:
        :return:
        """
        sql = f"""SELECT id, player_name, season, game_date, up, playing_time, pts, reb, oreb, dreb, ast, fga, fg, fg3a, fg3, fta, ft, stl, blk, tov, plus_minus, team, opp, game_win FROM public.player_regular_gamelog where player_name ='{player}' and up=True and season = {season} order by  game_date;
                                """
        games = get_sql(sql)
        if not len(games):
            return {
                'this_score': 0,
                'this_attend': 0,
                'this_hit_rate': (0, 1, 0, 1, 0, 1),
                'this_data': (0, 0, 0, 0, 0, 0),
                'this_fg': (0, 1),
                'this_fg3': (0, 1),
                'this_ft': (0, 1),
            }
        list_time = []
        total_win = total_loss = total_pts = total_rebs = total_asts = total_stls = total_tovs = total_blks = total_fg = total_fg3 = total_ft = 0
        total_fga = total_fg3a = total_fta = 1
        for game in games:
            total_pts += game.get('pts')
            total_rebs += game.get('reb')
            total_asts += game.get('ast')
            total_stls += game.get('stl')
            total_blks += game.get('blk')
            total_ft += game.get('ft')
            total_fta += game.get('fta')
            total_fg += game.get('fg')
            total_fga += game.get('fga')
            total_fg3 += game.get('fg3')
            total_fg3a += game.get('fg3a')
            total_tovs += game.get('tov')
            list_time.append(game.get('playing_time'))

            if game.get('game_win'):
                total_win += 1
            else:
                total_loss += 1

        total_time = sum(list_time, timedelta())

        # 计算平均值
        average_time = total_time / len(list_time)
        average_minutes, average_seconds = divmod(average_time.seconds, 60)

        if len(games) == 1:
            this_team = games[-1].get('team')
        else:
            this_team = games[-2].get('team')
        if this_team == 'PHO':
            this_team = 'PHX'
        ave = {
            'this_attend': len(games),
            'this_data': (
                round(total_pts / len(games), 1), round(total_rebs / len(games), 1),
                round(total_asts / len(games), 1), round(total_stls / len(games), 1),
                round(total_blks / len(games), 1), round(total_tovs / len(games), 1)),
            'this_hit_rate': (total_fg, total_fga, total_fg3, total_fg3a, total_ft, total_fta),
            'this_team': this_team,
            'this_win': total_win,
            'this_time': f"{average_minutes}:{str(average_seconds).zfill(2)}",
            'this_score': round(
                (total_pts + total_rebs + total_asts + total_stls + total_blks - total_tovs) / len(games), 1),
            'this_loss': total_loss
        }

        return ave

    def get_person_info(self, player_name):
        """
        查询基本数据，上赛季数据、本赛季数据、表现最佳赛季数据
        :param player_name:
        :return:
        """
        basic_info = self.get_basic_info(player_name)
        last_season_data = self.get_player_last_season_data(player_name)
        this_season_data = self.get_game_log_with_season(player_name, 2024)
        best_season_data = self.get_best_season(player_name)
        basic_info.update(last_season_data)
        basic_info.update(this_season_data)
        basic_info.update(best_season_data)
        return basic_info

    def get_best_season(self, player_name):
        """
        查询最佳表现
        :param player_name:
        :return:
        """
        sql = f"""
        SELECT *,
           (pts + reb + ast + stl + blk) / game_attend AS avg_performance
            FROM public.player_regular_total_season
            where player_name ='{player_name}'
            ORDER BY avg_performance DESC
            LIMIT 1;
                """
        best_season = get_sql(sql)
        this_season = self.get_game_log_with_season(player_name, 2024)

        sql = f"""
        SELECT COUNT(*) 
            FROM public.player_regular_total_season
            WHERE player_name  ='{player_name}';"""
        total_season = get_sql(sql)[0].get('count')
        if not len(best_season) or this_season.get('this_score') > best_season[0].get('avg_performance'):
            return {
                'total_season': total_season,
                "best_season": '2023-24',
                "best_team": this_season.get('this_team'),
                "best_season_game_attend": this_season.get('this_attend'),
                "best_data": this_season.get('this_data'),
                "best_hit_rate": this_season.get('this_hit_rate')
            }
        season = best_season[0].get('season')
        game_attend = best_season[0].get('game_attend')
        data = (
            round(best_season[0].get('pts') / game_attend, 1),
            round(best_season[0].get('reb') / game_attend, 1),
            round(best_season[0].get('ast') / game_attend, 1),
            round(best_season[0].get('stl') / game_attend, 1),
            round(best_season[0].get('blk') / game_attend, 1),
            round(best_season[0].get('tov') / game_attend, 1),

        )

        return {
            'total_season': total_season,
            "best_season": season,
            "best_team": best_season[0].get('team'),
            "best_season_game_attend": game_attend,
            "best_data": data,
            "best_hit_rate": (best_season[0].get('fg'), best_season[0].get('fga') if best_season[0].get('fga') else 1,
                              best_season[0].get('fg3'), best_season[0].get('fg3a') if best_season[0].get('fg3a') else 1,
                              best_season[0].get('ft'), best_season[0].get('fta') if best_season[0].get('fta') else 1)
        }

    def get_honor(self, player):
        honors = get_sql(f"select * from public.player_honors where player_name ='{player}' order by honor;")
        honor_list = []
        for item in honors:
            honor_list.append(item.get('honor'))
        print(honor_list)

        return '、'.join(honor_list)

    def get_salary(self, player):
        result = get_sql(f"select salary from public.player_salary where player_name='{player}' and season =2024;")
        if result:
            return f"**{int(result[0].get('salary') / 10000)}万美金**"
        else:
            return "暂无数据"


if __name__ == '__main__':
    player = "Amar'e Stoudemire"
    NbaUtils().get_honor(player.replace("'", "''"))
