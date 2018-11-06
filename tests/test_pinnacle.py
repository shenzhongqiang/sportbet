import unittest
import betdata.pinnacle

class Test(unittest.TestCase):
    def setUp(self):
        self.inst = betdata.pinnacle.Feed()

    def tearDown(self):
        pass

    def test_get_sports(self):
        result = self.inst.get_sports()

    def test_get_teams(self):
        result = self.inst.get_sports()
        teams = []
        for er in result:
            teams.extend(er.teams)
        teams = list(set(teams))
        for team in teams:
            print(team)
