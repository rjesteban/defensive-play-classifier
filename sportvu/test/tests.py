import unittest
import json
from sportvu.utils import *


PATH = 'data/test/'
testdata = json.load(open(PATH + '0021500391.json'))


class TestSportVUUtilFunctions(unittest.TestCase):

    def test_find_index(self):
        self.assertEqual(find_index(testdata, 272), 234)
        self.assertEqual(find_index(testdata, 1), 0)
        self.assertEqual(find_index(testdata, 485), 410)

    def test_get_moment(self):
        out27 = open(PATH + '27.out', 'r').read()
        out307 = open(PATH + '307.out', 'r').read()
        error_msg = "ids did not match"
        self.assertEqual(str(get_moment(testdata, 27)), out27, msg=error_msg)
        self.assertEqual(str(get_moment(testdata, 307)), out307, msg=error_msg)
        self.assertEqual(str(get_moment(testdata, 27)[0][0]), "1")
        self.assertEqual(str(get_moment(testdata, 307)[0][0]), "3")

    def test_get_players(self):
        home = str([[201166, 'G', 'home', 4], [2550, 'G', 'home', 4],
                    [201149, 'C', 'home', 4],
                    [202710, 'G-F', 'home', 4], [202703, 'F', 'home', 4]])
        away = str([[1626169, 'F', 'visitor', 4], [202694, 'F', 'visitor', 4],
                    [2581, 'G', 'visitor', 4],
                    [201229, 'F', 'visitor', 4], [201202, 'C', 'visitor', 4]])
        self.assertEqual(str(get_playersoncourt(testdata, 485)), home)
        self.assertEqual(str(get_playersoncourt(testdata,
                         485, side='away')), away)

    def test_determine_offs_defs(self):
        gameid = '0021500391'
        offense = get_playersoncourt(testdata, 4, side='visitor')  # pistons
        defense = get_playersoncourt(testdata, 4)  # bulls
        out = str({'offense': offense, 'defense': defense})
        self.assertEqual(str(determine_offs_defs(testdata, gameid, 4)), out)

        offense = get_playersoncourt(testdata, 108)  # bulls
        defense = get_playersoncourt(testdata, 108, side='visitor')  # pistons
        out = str({'offense': offense, 'defense': defense})
        self.assertEqual(str(determine_offs_defs(testdata, gameid, 108)), out)

        # 150 foul by home team (bulls)
        offense = get_playersoncourt(testdata, 150, side='visitor')  # pistons
        defense = get_playersoncourt(testdata, 150, side='home')  # bulls
        out = str({'offense': offense, 'defense': defense})
        self.assertEqual(str(determine_offs_defs(testdata, gameid, 150)), out)

        # 195 foul by away team (pistons)
        offense = get_playersoncourt(testdata, 195, side='home')  # bulls
        defense = get_playersoncourt(testdata, 195, side='visitor')  # pistons
        out = str({'offense': offense, 'defense': defense})
        self.assertEqual(str(determine_offs_defs(testdata, gameid, 195)), out)

        # 2 turnover by home team
        offense = get_playersoncourt(testdata, 2)
        defense = get_playersoncourt(testdata, 2, side='visitor')
        out = str({'offense': offense, 'defense': defense})
        self.assertEqual(str(determine_offs_defs(testdata, gameid, 2)), out)

        # 99 turnover by away team
        offense = get_playersoncourt(testdata, 99, side='visitor')
        defense = get_playersoncourt(testdata, 99)
        out = str({'offense': offense, 'defense': defense})
        self.assertEqual(str(determine_offs_defs(testdata, gameid, 99)), out)


if __name__ == '__main__':
    unittest.main()
