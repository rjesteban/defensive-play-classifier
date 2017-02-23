import unittest
import json
from utils import get_moment, get_playerposition

testdata = json.load(open('0021500391.json'))

class TestSportVUUtilMethods(unittest.TestCase):

    def test_get_moment(self):
        out27 = open('27.out', 'r').read()
        out307 = open('307.out', 'r').read()
        self.assertEqual(str(get_moment(testdata, 27)), out27)
        self.assertEqual(str(get_moment(testdata, 307)), out307)

    
    def test_get_playerposition(self):
        self.assertEqual(get_playerposition(testdata, 203083), 'C')
        self.assertEqual(get_playerposition(testdata, 202734), 'G')
        self.assertEqual(get_playerposition(testdata, 203503), 'F')
