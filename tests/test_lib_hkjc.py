import unittest
import betdata.hkjc

class Test(unittest.TestCase):
    def setUp(self):
        self.inst = betdata.hkjc.Feed()

    def tearDown(self):
        pass

    def test_get_sports(self):
        result = self.inst.get_sports()
        print(result)


