import math
import datetime
import re
import json
import requests
from lxml import etree
from event_result import EventResult

class Feed(object):
    def __init__(self):
        pass

    def get_odds(self, price_nodes):
        options = []
        for price_node in price_nodes:
            if price_node["side"] != "win":
                continue
            odds = float(price_node["decimal-odds"])
            options.append(odds)
        best_odds = max(options)
        return best_odds

    def get_sports(self):
        url = "https://api.matchbook.com/edge/rest/events"
        r = requests.get(url)
        content = r.content.decode("utf-8")
        root = json.loads(content)
        total = root["total"]
        per_page = 100
        num_page = math.ceil(total/per_page)
        result = []
        for i in range(num_page):
            offset = per_page * i
            page_result = self.get_sports_per_page(offset, per_page)
            result.extend(page_result)
        return result

    def get_sports_per_page(self, offset, per_page):
        url = "https://api.matchbook.com/edge/rest/events?offset={}&per-page={}".format(offset, per_page)
        r = requests.get(url)
        content = r.content.decode("utf-8")
        root = json.loads(content)
        total = root["total"]
        offset = root["offset"]
        per_page = root["per-page"]
        events = root["events"]
        print(per_page, offset, total)
        result = []
        for event in events:
            event_name = event["name"]
            start = event["start"]
            status = event["status"]
            dt = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ")
            er = EventResult(event_name)
            er.set_time(dt)
            markets = event["markets"]
            for market in markets:
                market_type = market["market-type"]
                if market_type != "money_line" and market_type != "one_x_two":
                    continue
                runners = market["runners"]
                for runner in runners:
                    name = runner["name"]
                    price_nodes = list(filter(lambda x: x["side"] == "win", runner["prices"]))
                    if len(price_nodes) == 0:
                        continue
                    odds = self.get_odds(price_nodes)
                    if re.match(r"DRAW", name, re.I):
                        er.add_odds("", odds, True)
                    else:
                        er.add_odds(name, odds, False)
                result.append(er)
        return result
