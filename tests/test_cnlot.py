import unittest
import betdata.cnlot

class Test(unittest.TestCase):
    def setUp(self):
        self.inst = betdata.cnlot.Feed()

    def tearDown(self):
        pass

    def test_get_teams(self):
        result = self.inst.get_teams("2018-11-05")


