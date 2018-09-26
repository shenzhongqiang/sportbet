import time
import datetime
import re
import json
import requests
from event_result import EventResult


class Feed(object):
    def __init__(self):
        pass

    def get_sports(self):
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
            er = EventResult(league)
            er.set_time(dt)
            if "had" not in v:
                continue
            draw_odds = float(v["had"]["d"])
            away_odds = float(v["had"]["a"])
            home_odds = float(v["had"]["h"])
            er.add_odds("", draw_odds, True)
            er.add_odds(away_team, away_odds, False)
            er.add_odds(home_team, home_odds, False)
            result.append(er)
        return result
