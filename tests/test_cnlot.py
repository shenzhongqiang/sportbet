import unittest
import betdata.cnlot

class Test(unittest.TestCase):
    def setUp(self):
        self.inst = betdata.cnlot.Feed()

    def tearDown(self):
        pass

    def test_get_dates(self):
        result = self.inst.get_dates()

    def test_get_games(self):
        result = self.inst.get_games("2018-11-05")

    def test_get_teams(self):
        teams = self.inst.get_teams()

