import datetime
import re
import json
import base64
import requests
from lxml import etree
from event_result import EventResult

class Feed(object):
    def __init__(self):
        pass

    def get_sports(self):
        url = "http://lines.bookmaker.eu/"
        r = requests.get(url)
        content = r.content.decode("utf-8")
        root = etree.fromstring(content)
        league_nodes = root.xpath('/Data/Leagues/league')
        result = []
        for league_node in league_nodes:
            league_name = league_node.attrib["Description"]
            line_nodes = league_node.xpath('./game/line')
            ers = self.get_games(league_node)
            result.extend(ers)
        return result

    def get_games(self, league_node):
        league_name = league_node.attrib["Description"]
        game_nodes = league_node.xpath('./game')
        result = []
        for game_node in game_nodes:
            team_a = game_node.attrib["vtm"]
            team_b = game_node.attrib["htm"]
            gmdt = game_node.attrib["gmdt"]
            gmtm = game_node.attrib["gmtm"]
            str_time = "{} {}".format(gmdt, gmtm)
            dt = datetime.datetime.strptime(str_time, "%Y%m%d %H:%M:%S")
            if team_a == "" or team_b == "":
                continue
            line_nodes = game_node.xpath('./line')
            if len(line_nodes) > 1:
                print("need investigate - multiple lines for game between {} {}".format(team_a, team_b))
                continue
            er = EventResult(league_name)
            er.set_time(dt)
            line_node = line_nodes[0]
            a_odds = line_node.attrib["voddst"]
            b_odds = line_node.attrib["hoddst"]
            draw_odds = line_node.attrib["vspoddst"]
            er.add_odds(team_a, a_odds, False)
            er.add_odds(team_b, b_odds, False)
            er.add_odds("", draw_odds, True)
            result.append(er)
        return result
