import unittest
import json
from utils import get_moment, get_playerposition, get_distance

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

    def test_get_distance(self):
        x1, y1, x2, y2 = 27.35625, 12.54398, 36.06287, 29.64372
        i1, j1, i2, j2 = 1.46202, 34.72808, 17.48111, 46.11693
        d1, d2 = 19.1887, 19.65495
        self.assertAlmostEqual(get_distance((x1, y1), (x2, y2)), d1, places=4)
        self.assertAlmostEqual(get_distance((i1, j1), (i2, j2)), d2, places=4)
