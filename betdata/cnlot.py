import re
import datetime
import requests
import lxml.html
from lib.event_result import Match

class Feed(object):
    def __init__(self):
        pass

    def get_dates(self):
        url = "http://www.lottery.gov.cn/football/counter.jspx"
        r = requests.get(url)
        content = r.content.decode("utf-8")
        root = lxml.html.fromstring(content)
        li_nodes = root.xpath('.//ul[@id="historyUL"]/li')
        dates = []
        for node in li_nodes:
            text = node.text
            matched = re.search(r"(\d+\-\d+\-\d+)", text)
            date = matched.group(1)
            dates.append(date)
        return dates

    def get_games(self, date_str):
        url = "http://www.lottery.gov.cn/football/counter.jspx?date={}".format(date_str)
        r = requests.get(url)
        content = r.content.decode("utf-8")
        root = lxml.html.fromstring(content)
        section_nodes = root.xpath('.//div[@class="section"]')
        result = []
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
            home_win_text = td_nodes[5].xpath('./strong')[0].text
            draw_text = td_nodes[6].xpath('./strong')[0].text
            away_win_text = td_nodes[7].xpath('./strong')[0].text
            if home_win_text is not None \
                and draw_text is not None and away_win_text is not None:
                home_win = float(home_win_text)
                draw = float(draw_text)
                away_win = float(away_win_text)
                match = Match(league=league, team_home=team_home, team_away=team_away,
                    handicap="0", home_win=home_win, away_win=away_win, draw=draw, time=dt)
                result.append(match)

            handicap = td_nodes[8].xpath('./strong/font')[0].text
            home_win_text = td_nodes[9].xpath('./strong')[0].text
            draw_text = td_nodes[10].xpath('./strong')[0].text
            away_win_text = td_nodes[11].xpath('./strong')[0].text
            if home_win_text is not None \
                and draw_text is not None and away_win_text is not None:
                home_win = float(home_win_text)
                draw = float(draw_text)
                away_win = float(away_win_text)
                match = Match(league=league, team_home=team_home, team_away=team_away,
                    handicap=handicap, home_win=home_win, away_win=away_win, draw=draw, time=dt)
                result.append(match)
        return result

    def get_team_page_num(self):
        url = "http://www.lottery.gov.cn/football/result.jspx"
        now = datetime.datetime.now()
        today = now.strftime("%Y-%m-%d")
        year = datetime.timedelta(days=365)
        today_lastyear = (now - year).strftime("%Y-%m-%d")
        data = {
            "f_league_id": "0",
            "f_league_name": "全部联赛",
            "startDate": today_lastyear,
            "endDate": today,
        }
        r = requests.post(url, data=data)
        content = r.content.decode("utf-8")
        matched = re.search(r"共(\d+)条记录 \d+/(\d+)页", content, re.M)
        record_num = matched.group(1)
        page_num = matched.group(2)
        return int(page_num)

    def get_teams(self):
        page_num = self.get_team_page_num()
        teams = []
        for i in range(1, page_num+1, 1):
            url = "http://www.lottery.gov.cn/football/result_{}.jspx".format(i)
            now = datetime.datetime.now()
            today = now.strftime("%Y-%m-%d")
            year = datetime.timedelta(days=365)
            today_lastyear = (now - year).strftime("%Y-%m-%d")
            data = {
                "f_league_id": "0",
                "f_league_name": "全部联赛",
                "startDate": today_lastyear,
                "endDate": today,
            }
            r = requests.post(url, data=data)
            content = r.content.decode("utf-8")
            root = lxml.html.fromstring(content)
            home_nodes = root.xpath('.//div[@class="xxsj"]/table//span[@class="zhu"]')
            away_nodes = root.xpath('.//div[@class="xxsj"]/table//span[@class="ke"]')
            home_teams = list(map(lambda x: x.text, home_nodes))
            away_teams = list(map(lambda x: x.text, away_nodes))
            teams.extend(home_teams)
            teams.extend(away_teams)
            teams = list(set(teams))
            print(i, len(teams))
            print(teams)
