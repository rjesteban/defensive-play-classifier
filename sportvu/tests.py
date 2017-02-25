import unittest
import json
from utils import get_moment, get_playerposition

testdata = json.load(open('0021500391.json'))


class TestSportVUUtilFunctions(unittest.TestCase):

    def test_get_moment(self):
        out27 = open('27.out', 'r').read()
        out307 = open('307.out', 'r').read()
        error_msg = "ids did not match"
        self.assertEqual(str(get_moment(testdata, 27)), out27, msg=error_msg)
        self.assertEqual(str(get_moment(testdata, 307)), out307, msg=error_msg)

    def test_get_playerposition(self):
        self.assertEqual(get_playerposition(testdata, 203083), 'C')
        self.assertEqual(get_playerposition(testdata, 202734), 'G')
        self.assertEqual(get_playerposition(testdata, 203503), 'F')


if __name__ == '__main__':
    unittest.main()
