import datetime
import re
import json
import requests
import zlib
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
        url = "https://odds.smarkets.com/oddsfeed.xml.gz"
        r = requests.get(url)

        content = zlib.decompress(r.content, zlib.MAX_WBITS|32)
        root = etree.fromstring(content)
        event_nodes = root.xpath('/odds/event')
        result = []
        for event_node in event_nodes:
            event_name = event_node.attrib["name"]
            parent_name = event_node.attrib["parent_name"]
            event_date = event_node.attrib["date"]
            event_time = event_node.attrib["time"]
            str_time = "{} {}".format(event_date, event_time)
            dt = datetime.datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
            er = EventResult(parent_name)
            market_nodes = event_node.xpath('./market[@slug="winner"]')
            if len(market_nodes) == 0:
                print("no markets for {}".format(name))
                continue
            market_node = market_nodes[0]
            contract_nodes = market_node.xpath('./contract')
            for contract_node in contract_nodes:
                name = contract_node.get("name", "")
                is_draw = name == "Draw"
                odds = self.get_odds(contract_node)
                er.set_time(dt)
                if is_draw:
                    er.add_odds("", odds, True)
                else:
                    er.add_odds(name, odds, False)
            result.append(er)
        return result
