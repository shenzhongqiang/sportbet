import unittest
import betdata.sporttery

class Test(unittest.TestCase):
    def setUp(self):
        self.inst = betdata.sporttery.Feed()

    def tearDown(self):
        pass

    def test_get_games(self):
        result = self.inst.get_games()
        print(result)

