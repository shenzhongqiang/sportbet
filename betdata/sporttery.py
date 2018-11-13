import time
import datetime
import re
import json
import requests
from event_result import Match
import lib.team_name


class Feed(object):
    def __init__(self):
        self.source = "sporttery"

    def get_games(self):
        ts = int(time.time() * 1000)
        url = "http://i.sporttery.cn/odds_calculator/get_odds?i_format=json&i_callback=getData&poolcode[]=hhad&poolcode[]=had&_={}".format(ts)
        r = requests.get(url)
        content = r.content.decode("utf-8")
        matched = re.match(r"getData\((.*?)\)", content, re.M)
        if not matched:
            msg = "error getting data from {}".format(url)
            raise Exception(msg)

        json_data = matched.group(1)
        data = json.loads(json_data)
        result = []
        for k, v in data["data"].items():
            start_time = "{} {}".format(v["date"], v["time"])
            dt = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            league = v["l_cn"]
            home_team = v["h_cn"]
            away_team = v["a_cn"]
            home_team_en = lib.team_name.cnzh2en(home_team)
            away_team_en = lib.team_name.cnzh2en(away_team)
            home_win = float(v["had"]["h"])
            away_win = float(v["had"]["a"])
            draw = float(v["had"]["d"])
            match = Match(source=self.source, league=league, team_home=home_team_en, team_away=away_team_en,
                handicap="0", home_win=home_win, away_win=away_win, draw=draw, time=dt)
            result.append(match)
            home_win = float(v["hhad"]["h"])
            away_win = float(v["hhad"]["a"])
            draw = float(v["hhad"]["d"])
            handicap = v["hhad"]["fixedodds"]
            match = Match(source=self.source, league=league, team_home=home_team_en, team_away=away_team_en,
                handicap=handicap, home_win=home_win, away_win=away_win, draw=draw, time=dt)
            result.append(match)
        return result

