import datetime
import re
import json
import base64
import requests
from event_result import EventResult, Match

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
        #r = requests.get(url, headers=headers, verify=False, proxies=proxies)
        r = requests.get(url, headers=headers, verify=False)
        content = r.content.decode("utf-8")
        events = json.loads(content)
        result = []
        for event in events:
            match_time = event["matchTime"].split("+")[0]
            dt = datetime.datetime.strptime(match_time, "%Y-%m-%dT%H:%M:%S")
            home_team = event["homeTeam"]["teamNameEN"]
            away_team = event["awayTeam"]["teamNameEN"]
            league = event["league"]["leagueNameEN"]
            home_win = None
            away_win = None
            draw = None
            for k, v in event["hadodds"].items():
                if k == "D":
                    draw = float(v.split("@")[1])
                elif k == "A":
                    away_win = float(v.split("@")[1])
                elif k == "H":
                    home_win = float(v.split("@")[1])
            match = Match(league=league, team_home=home_team, team_away=away_team,
                handicap="0", home_win=home_win, away_win=away_win, draw=draw, time=match_time)
            result.append(match)
        return result

    def get_handicap_sports(self):
        url = "https://bet.hkjc.com/football/getJSON.aspx?jsontype=odds_hha.aspx"
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
        r = requests.get(url, headers=headers, verify=False)
        content = r.content.decode("utf-8")
        events = json.loads(content)
        events = list(filter(lambda x: x["name"] == "ActiveMatches", events))[0]["matches"]
        result = []
        for event in events:
            match_time = event["matchTime"].split("+")[0]
            dt = datetime.datetime.strptime(match_time, "%Y-%m-%dT%H:%M:%S")
            home_team = event["homeTeam"]["teamNameEN"]
            away_team = event["awayTeam"]["teamNameEN"]
            league = event["league"]["leagueNameEN"]
            home_win = None
            away_win = None
            draw = None
            for k, v in event["hhaodds"].items():
                if k == "D":
                    draw = float(v.split("@")[1])
                elif k == "A":
                    away_win = float(v.split("@")[1])
                elif k == "H":
                    home_win = float(v.split("@")[1])
            handicap_hg = event["hhaodds"]["HG"]
            handicap_ag = event["hhaodds"]["AG"]
            if int(handicap_hg) + int(handicap_ag) != 0:
                msg = "handicap HG is {} and AG is {}".format(handicap_hg, handicap_ag)
                raise Exception(msg)
            match = Match(league=league, team_home=home_team, team_away=away_team,
                handicap=handicap_hg, home_win=home_win, away_win=away_win, draw=draw, time=match_time)
            result.append(match)
        return result
