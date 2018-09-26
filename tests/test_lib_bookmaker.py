import unittest
import betdata.bookmaker

class Test(unittest.TestCase):
    def setUp(self):
        self.inst = betdata.bookmaker.Feed()

    def tearDown(self):
        pass

    def test_get_sports(self):
        result = self.inst.get_sports()
        print(result)

