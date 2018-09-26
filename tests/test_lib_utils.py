import unittest
import lib.utils

class Test(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_team_encn_mapping(self):
        mapping = lib.utils.get_team_encn_mapping()
        print(mapping)

    def test_get_team_cnen_mapping(self):
        mapping = lib.utils.get_team_cnen_mapping()
        print(mapping)

    def test_get_team_cn(self):
        cn = lib.utils.get_team_cn()
        print(cn)

    def test_get_team_en(self):
        en = lib.utils.get_team_en()
        print(en)
