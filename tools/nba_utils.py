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
            return {'last_score': 0}

        hit_rate = ''
        if player_data[0].get('fga'):
            hit_rate += f"投篮{round(player_data[0].get('fg') / player_data[0].get('fga') * 100, 1)}%，"
        if player_data[0].get('fg3a'):
            hit_rate += f"三分{round(player_data[0].get('fg3') / player_data[0].get('fg3a') * 100, 1)}%，"
        if player_data[0].get('fta'):
            hit_rate += f"罚球{round(player_data[0].get('ft') / player_data[0].get('fta') * 100, 1)}%"

        attend = player_data[0].get('game_attend')
        data_detail = f"{round(player_data[0].get('pts') / attend, 1)}分 | {round(player_data[0].get('reb') / attend, 1)}篮板 | {round(player_data[0].get('ast') / attend, 1)}助攻 | {round(player_data[0].get('stl') / attend, 1)}抢断 | {round(player_data[0].get('blk') / attend, 1)}盖帽"
        salary = f"{int(player_data[0].get('salary') / 10000)}万美金" if player_data[0].get('salary') else "暂无数据"
        team = player_data[0].get('team')

        return {
            'last_attend': attend,
            'last_data': data_detail,
            'last_hit_rate': hit_rate,
            'last_salary': salary,
            'last_team': team,
            'last_score': round(
                (player_data[0].get('pts') + player_data[0].get('reb') + player_data[0].get('ast') +
                 player_data[0].get('stl') + player_data[0].get('blk')) / attend, 1)
        }

    def get_game_data(self, sql):
        games = get_sql(sql)
        hit_rate = ''
        total_win = total_loss = total_pts = total_rebs = total_asts = total_stls = total_tovs = total_blks = total_fga = total_fg = total_fg3 = total_fg3a = total_ft = total_fta = 0

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
            if game.get('game_win'):
                total_win += 1
            else:
                total_loss += 1

        if total_fga:
            hit_rate += f"投篮{round(total_fg / total_fga * 100, 1)}%，"
        if total_fg3a:
            hit_rate += f"三分{round(total_fg3 / total_fg3a * 100, 1)}%，"
        if total_fta:
            hit_rate += f"罚球{round(total_ft / total_fta * 100, 1)}%"
        ave = {
            'data': {
                '得分：': round(total_pts / len(games), 1),
                '篮板：': round(total_rebs / len(games), 1),
                '助攻：': round(total_asts / len(games), 1),
                '抢断：': round(total_stls / len(games), 1),
                '盖帽：': round(total_blks / len(games), 1),
                '失误：': round(total_tovs / len(games), 1),
            },
            'this_fg': (total_fg, total_fga),
            'this_fg3': (total_fg3, total_fg3a),
            'this_ft': (total_ft, total_fta),
            'hit_rate': hit_rate,
            'win': total_win,
            'score': round(
                (total_pts + total_rebs + total_asts + total_stls + total_blks - total_tovs - total_fga) / (
                        total_fga * len(games)), 1),
            'loss': total_loss
        }

        return ave

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
                ARRAY_AGG(DISTINCT team) AS teams_played_for
            FROM
                public.player_regular_gamelog
            WHERE
                player_name = '{player_name}' and up=true
            GROUP BY
                player_name;
            """
        result = get_sql(sql)
        hit_rate = (round(result[0].get('total_fg') * 100 / result[0].get('total_fga'), 1),
                    round(result[0].get('total_fg3') * 100 / (result[0].get('total_fg3a') if result[0].get(
                        'total_fg3a') else 1), 1),
                    round(result[0].get('total_ft') * 100 / result[0].get('total_fta'), 1))
        data = (round(result[0].get('total_points') / result[0].get('total_games'), 1),
                round(result[0].get('total_rebounds') / result[0].get('total_games'), 1),
                round(result[0].get('total_assists') / result[0].get('total_games'), 1),
                round(result[0].get('total_blocks') / result[0].get('total_games'), 1),
                round(result[0].get('total_steals') / result[0].get('total_games'), 1),
                round(result[0].get('total_tovs') / result[0].get('total_games'), 1)
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
            'code': basic_info.get('code'),
            'chinese_name': basic_info.get('chinese_name'),
            'draft_year': basic_info.get('draft_year'),
            'draft_position': basic_info.get('draft_position'),
            'draft_team': draft_team,
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
        hit_rate = ''
        if not len(games):
            return {
                'this_score': 0,
                'this_attend': 0,
                'this_hit_rate': hit_rate,
                'this_data': (0, 0, 0, 0, 0, 0),
                'this_fg': (0, 1),
                'this_fg3': (0, 1),
                'this_ft': (0, 1),
            }

        total_win = total_loss = total_pts = total_rebs = total_asts = total_stls = total_tovs = total_blks = total_fga = total_fg = total_fg3 = total_fg3a = total_ft = total_fta = 0
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

            if game.get('game_win'):
                total_win += 1
            else:
                total_loss += 1

        if total_fga:
            hit_rate += f"投篮{round(total_fg / total_fga * 100, 1)}%，"
        if total_fg3a:
            hit_rate += f"三分{round(total_fg3 / total_fg3a * 100, 1)}%，"
        if total_fta:
            hit_rate += f"罚球{round(total_ft / total_fta * 100, 1)}%"

        if len(games) == 1:
            this_team = games[-1].get('team')
        else:
            this_team = games[-2].get('team')
        ave = {
            'this_attend': len(games),
            'this_data': (
                round(total_pts / len(games), 1), round(total_rebs / len(games), 1),
                round(total_asts / len(games), 1), round(total_stls / len(games), 1),
                round(total_blks / len(games), 1), round(total_tovs / len(games), 1)),
            'this_fg': (total_fg, total_fga),
            'this_fg3': (total_fg3, total_fg3a),
            'this_ft': (total_ft, total_fta),
            'this_hit_rate': hit_rate,
            'this_team': this_team,
            'this_win': total_win,
            'this_score': round(
                (total_pts + total_rebs + total_asts + total_stls + total_blks) / len(games), 1),
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
        sql = f"""
        SELECT COUNT(*) 
            FROM public.player_regular_total_season
            WHERE player_name  ='{player_name}';"""
        total_season = get_sql(sql)[0].get('count')
        season = best_season[0].get('season')
        game_attend = best_season[0].get('game_attend')
        data = {
            '得分：': round(best_season[0].get('pts') / game_attend, 1),
            '篮板：': round(best_season[0].get('reb') / game_attend, 1),
            '助攻：': round(best_season[0].get('ast') / game_attend, 1),
            '抢断：': round(best_season[0].get('stl') / game_attend, 1),
            '盖帽：': round(best_season[0].get('blk') / game_attend, 1),
            '失误：': round(best_season[0].get('tov') / game_attend, 1),

        }
        fg = (best_season[0].get('fg'), best_season[0].get('fga'))
        fg3 = (best_season[0].get('fg3'), best_season[0].get('fg3a'))
        ft = (best_season[0].get('ft'), best_season[0].get('fta'))
        best_hit_rate = ''
        best_hit_rate += f"投篮{round(fg[0] / fg[1] * 100, 1)}%，"
        if fg3[1]:
            best_hit_rate += f"三分{round(fg3[0] / fg3[1] * 100, 1)}%，"
        if ft[1]:
            best_hit_rate += f"罚球{round(ft[0] / ft[1] * 100, 1)}%"
        return {
            'total_season': total_season,
            "best_season": season,
            "best_team": best_season[0].get('team'),
            "best_season_game_attend": game_attend,
            "best_data": data,
            "best_fg": fg,
            "best_ft": ft,
            "best_fg3": fg3,
            "best_hit_rate": best_hit_rate
        }


if __name__ == '__main__':
    NbaUtils().get_game_log_with_team('James Harden', 'PHI')
