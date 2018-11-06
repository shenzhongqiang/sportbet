class Odds(object):
    def __init__(self, team, odds, is_draw):
        self.team = team
        self.odds = odds
        self.is_draw = is_draw

    def __repr__(self):
        return '<Odds team="{}" odds={} is_draw={}>'.format(self.team, self.odds, self.is_draw)

class EventResult(object):
    def __init__(self, league):
        self.league = league
        self.teams = []
        self.odds = []
        self.time = None

    def set_time(self, dt):
        self.time = dt

    def add_odds(self, team, odds, is_draw):
        odds = Odds(team, odds, is_draw)
        self.odds.append(odds)
        if is_draw == False:
            self.teams.append(team)

    def __repr__(self):
        str_teams = "[" + ", ".join(self.teams) + "]"
        str_odds = ""
        for item in self.odds:
            str_odds += item.__repr__()

        str_odds = "[" + str_odds + "]"
        return '<EventResult league="{}" time="{}" teams={} odds={}>'.format(self.league, self.time, str_teams, str_odds)

class Match(object):
    def __init__(self, league, team_home, team_away, handicap, home_win, away_win, draw, time):
        self.league = league
        self.team_home = team_home
        self.team_away = team_away
        self.handicap = handicap
        self.home_win = home_win
        self.away_win = away_win
        self.draw = draw
        self.time = time

    def get_teams(self):
        teams = [self.team_home, self.team_away]
        return teams

    def __repr__(self):
        return '<Match league="{}" team_home="{}" team_away="{}" handicap="{}" home_win="{}" away_win="{}" draw="{}" time="{}">'.format(self.league, self.team_home, self.team_away, self.handicap, self.home_win, self.away_win, self.draw, self.time)

class TotalResult(object):
    pass
