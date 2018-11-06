import datetime
import requests
import lxml.html
from lib.event_result import Match

class Feed(object):
    def __init__(self):
        pass

    def get_teams(self, date_str):
        url = "http://www.lottery.gov.cn/football/counter.jspx?date={}".format(date_str)
        r = requests.get(url)
        content = r.content.decode("utf-8")
        root = lxml.html.fromstring(content)
        section_nodes = root.xpath('.//div[@class="section"]')
        for node in section_nodes:
            td_nodes = node.xpath('.//table[@class="saishi"]/tr/td')
            league = td_nodes[1].text
            time_node = td_nodes[2]
            mon_day = time_node.text
            time = time_node.xpath('./br')[0].tail
            datetime_str = "2018-{} {}".format(mon_day, time)
            dt = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            team_home = td_nodes[3].text
            team_away = td_nodes[4].text
            home_win = float(td_nodes[5].xpath('./strong')[0].text)
            draw = float(td_nodes[6].xpath('./strong')[0].text)
            away_win = float(td_nodes[7].xpath('./strong')[0].text)
            match = Match(league=league, team_home=team_home, team_away=team_away,
                handicap="0", home_win=home_win, away_win=away_win, draw=draw, time=dt)

            handicap = td_nodes[8].xpath('./strong/font')[0].text
            home_win = float(td_nodes[9].xpath('./strong')[0].text)
            draw = float(td_nodes[10].xpath('./strong')[0].text)
            away_win = float(td_nodes[11].xpath('./strong')[0].text)
            match = Match(league=league, team_home=team_home, team_away=team_away,
                handicap=handicap, home_win=home_win, away_win=away_win, draw=draw, time=dt)
            print(match)
