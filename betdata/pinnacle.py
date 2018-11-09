import datetime
import re
import json
import base64
import requests
from lib.event_result import Match

def moneyline2odds(num):
    if num < 0:
        return -100/num + 1
    else:
        return num/100 + 1

class Feed(object):
    def __init__(self):
        user = "ZS1059152"
        passwd = "P58862455!"
        userpass = "%s:%s" % (user, passwd)
        token = base64.b64encode(userpass.encode("utf-8"))
        self.headers = {"Authorization": "Basic " + token.decode("utf-8")}

    def get_sports_v2(self):
        url = "https://api.pinnacle.com/v2/sports"
        r = requests.get(url, headers=self.headers, verify=False)
        content = r.content.decode("utf-8")
        data = json.loads(content)
        print(data)

    def get_sports(self):
        url = "https://www.pinnacle.com/webapi/1.17/api/v1/GuestLines/Today/29?callback=angular.callbacks._0"
        r = requests.get(url, headers=self.headers, verify=False)
        content = r.content.decode("utf-8")
        patt = re.compile(r"\((.*)\);")
        matched = patt.search(content)
        if not matched:
            raise Exception("get sports returns nothing")
        data = json.loads(matched.group(1))
        if data["OddsType"] != "american":
            raise Exception("odds type is not american")
        leagues = data["Leagues"]
        result = []
        for league in leagues:
            league_name = league["LeagueName"]
            events = league["Events"]
            ers = self.get_event_odds(league_name, events)
            result.extend(ers)
        return result

    def is_bettable(self, event):
        participants = event["Participants"]
        is_bettable = True
        for item in participants:
            if "MoneyLine" not in item:
                is_bettable = False
                break
        return is_bettable

    def get_event_odds(self, league_name, events):
        result = []
        for event in events:
            if not self.is_bettable(event):
                continue
            participants = event["Participants"]
            event_time = event["DateAndTime"]
            dt = datetime.datetime.strptime(event_time, "%Y-%m-%dT%H:%M:%SZ")
            er = EventResult(league_name)
            er.set_time(dt)
            for item in participants:
                team_name = item.get("Name", "")
                moneyline = item["MoneyLine"]
                is_draw = item["IsDraw"]
                odds = moneyline2odds(moneyline)
                er.add_odds(team_name, odds, is_draw)

            result.append(er)
        return result
