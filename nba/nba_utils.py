from nba.constants import nba_teams
from nba.sqlUtils import get_sql


def get_player_last_season_data(player_name):
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
    team = nba_teams.get(player_data[0].get('team'))

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


def get_game_data(sql):
    games = get_sql(sql)
    hit_rate = ''
    total_win = total_loss = total_pts = total_rebs = total_asts = total_stls = total_blks = total_fga = total_fg = total_fg3 = total_fg3a = total_ft = total_fta = 0

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
            '盖帽：': round(total_blks / len(games), 1)

        },
        'hit_rate': hit_rate,
        'win': total_win,
        'score': round(
            (total_pts + total_rebs + total_asts + total_stls + total_blks) / len(games), 1),
        'loss': total_loss
    }

    return ave


def get_game_log_with_team(player, team):
    sql = f"""SELECT id, player_name, season, game_date, up, playing_time, pts, reb, oreb, dreb, ast, fga, fg, fg3a, fg3, fta, ft, stl, blk, tov, plus_minus, team, opp, game_win FROM public.player_regular_gamelog where player_name ='{player}' and up=True and team = '{team}' order by  game_date;
                            """
    games = get_sql(sql)
    max_pts = max_rebs = max_asts = max_stls = max_blks = 0
    total_pts = total_rebs = total_asts = total_stls = total_blks = 0
    max_games = {}
    for game in games:
        total_pts += game.get('pts')
        total_rebs += game.get('reb')
        total_asts += game.get('ast')
        total_stls += game.get('stl')
        total_blks += game.get('blk')

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
        'blks': round(total_blks / len(games), 1)
    }

    return max_games, ave


def handle_game(game):
    attend = str(game.get('playing_time'))[2:]
    game_date = game.get('game_date')
    sum = game.get('pts') + game.get('reb') + game.get('ast') + game.get(
        'stl') + game.get('blk')
    data_detail = f"**{game.get('pts')}分 | {game.get('reb')}篮板 | {game.get('ast')}助攻 | {game.get('stl')}抢断 | {game.get('blk')}盖帽**"
    hit_rate = f"投篮{game.get('fg')}/{game.get('fga')}，三分球{game.get('fg3')}/{game.get('fg3a')}，罚球{game.get('ft')}/{game.get('fta')}"
    team = nba_teams.get(game.get('team'))
    return {
        'attend': attend,
        'data': data_detail,
        'hit_rate': hit_rate,
        'game_date': game_date,
        'team': team,
        'sum': sum,
        'opp': nba_teams.get(game.get('opp')),
        'result': game.get('game_win')
    }


def get_basic_info(player_name):
    sql = f"""select * from public.player_active where player_name='{player_name}'"""
    basic_info = get_sql(sql)[0]
    return {
        'code': basic_info.get('code'),
        'chinese_name': basic_info.get('chinese_name'),
        'draft_year': basic_info.get('draft_year'),
        'draft_position': basic_info.get('draft_position'),
        'this_team': basic_info.get('team')
    }


def get_game_log_with_season(player, season):
    sql = f"""SELECT id, player_name, season, game_date, up, playing_time, pts, reb, oreb, dreb, ast, fga, fg, fg3a, fg3, fta, ft, stl, blk, tov, plus_minus, team, opp, game_win FROM public.player_regular_gamelog where player_name ='{player}' and up=True and season = {season} order by  game_date;
                            """
    games = get_sql(sql)
    if not len(games):
        return {
            'this_score': 0
        }
    hit_rate = ''
    total_win = total_loss = total_pts = total_rebs = total_asts = total_stls = total_blks = total_fga = total_fg = total_fg3 = total_fg3a = total_ft = total_fta = 0
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
        'this_attend': len(games),
        'this_data': (
            round(total_pts / len(games), 1), round(total_rebs / len(games), 1),
            round(total_asts / len(games), 1),
            round(total_stls / len(games), 1), round(total_blks / len(games), 1)),
        'this_hit_rate': hit_rate,
        'this_win': total_win,
        'this_score': round(
            (total_pts + total_rebs + total_asts + total_stls + total_blks) / len(games), 1),
        'this_loss': total_loss
    }

    return ave


def get_person_info(player_name):
    basic_info = get_basic_info(player_name)
    last_season_data = get_player_last_season_data(player_name)
    this_season_data = get_game_log_with_season(player_name, 2024)
    basic_info.update(last_season_data)
    basic_info.update(this_season_data)
    return basic_info


if __name__ == '__main__':
    get_game_log_with_team('James Harden', 'PHI')
