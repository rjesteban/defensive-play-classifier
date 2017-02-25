import unittest
import json
from sportvu.utils import find_index, get_moment, get_playersoncourt

testdata = json.load(open('sportvu/0021500391.json'))


class TestSportVUUtilFunctions(unittest.TestCase):

    def test_find_index(self):
        self.assertEqual(find_index(testdata, 272), 234)
        self.assertEqual(find_index(testdata, 1), 0)
        self.assertEqual(find_index(testdata, 485), 410)

    def test_get_moment(self):
        out27 = open('sportvu/27.out', 'r').read()
        out307 = open('sportvu/307.out', 'r').read()
        error_msg = "ids did not match"
        self.assertEqual(str(get_moment(testdata, 27)), out27, msg=error_msg)
        self.assertEqual(str(get_moment(testdata, 307)), out307, msg=error_msg)

    def test_get_players(self):
        home = str([[201166, 'G'], [2550, 'G'], [201149, 'C'],
                    [202710, 'G-F'], [202703, 'F']])
        away = str([[1626169, 'F'], [202694, 'F'], [2581, 'G'],
                    [201229, 'F'], [201202, 'C']])
        self.assertEqual(str(get_playersoncourt(testdata, 485)), home)
        self.assertEqual(str(get_playersoncourt(testdata,
                         485, side='away')), away)


if __name__ == '__main__':
    unittest.main()
