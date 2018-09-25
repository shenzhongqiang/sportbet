import datetime
import re
import json
import base64
import requests
from event_result import EventResult

def moneyline2odds(num):
    if num < 0:
        return -100/num + 1
    else:
        return num/100 + 1

class Feed(object):
    def __init__(self):
        pass

    def get_sports(self):
        url = "https://bet.hkjc.com/football/getJSON.aspx?jsontype=index.aspx"
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Host": "bet.hkjc.com",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "If-None-Match": "WA86bd1f4e1fec3c54"
        }
        proxies = {
            "http": "http://127.0.0.1:1087",
            "https": "http://127.0.0.1:1087",
        }
        r = requests.get(url, headers=headers, verify=False, proxies=proxies)
        content = r.content.decode("utf-8")
        events = json.loads(content)
        result = []
        for event in events:
            match_time = event["matchTime"].split("+")[0]
            dt = datetime.datetime.strptime(match_time, "%Y-%m-%dT%H:%M:%S")
            home_team = event["homeTeam"]["teamNameEN"]
            away_team = event["awayTeam"]["teamNameEN"]
            league = event["league"]["leagueNameEN"]
            er = EventResult(league)
            er.set_time(dt)
            for k, v in event["hadodds"].items():
                if k == "D":
                    odds = float(v.split("@")[1])
                    er.add_odds("", odds, True)
                elif k == "A":
                    odds = float(v.split("@")[1])
                    er.add_odds(away_team, odds, False)
                elif k == "H":
                    odds = float(v.split("@")[1])
                    er.add_odds(home_team, odds, False)
            result.append(er)
        return result
