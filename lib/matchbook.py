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

    def get_odds(self, contract_node):
        price_nodes = contract_node.xpath('./bids/price')
        best_odds = float("inf")
        for price_node in price_nodes:
            odds = float(price_node.attrib["decimal"])
            if odds < best_odds:
                best_odds = odds
        return best_odds

    def get_sports(self):
        url = "https://api.matchbook.com/edge/rest/events"
        r = requests.get(url)
        content = r.content.decode("utf-8")
        root = json.loads(content)
        total = root["total"]
        per_page = 20
        num_page = math.ceil(total/per_page)
        result = []
        for i in range(num_page):
            offset = per_page * i
            page_result = self.get_sports_per_page(offset, per_page)
            result.extend(page_result)
            break
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
            markets = event["markets"]
            for market in markets:
            market_type = event["market-type"]
            if market_type != "money_line":
                continue
            print(json.dumps(event, indent=4))
            start = event["start"]
            status = event["status"]
            dt = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ")
            result.append(er)

