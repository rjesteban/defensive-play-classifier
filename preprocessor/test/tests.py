from preprocessor.utils import get_distance  # , arrange_by_position
import json
import unittest

testdata = json.load(open('data/sportvu/0021500582.json'))


class TestPreprocessorFunctions(unittest.TestCase):

    def test_get_distance(self):
        x1, y1, x2, y2 = 27.35625, 12.54398, 36.06287, 29.64372
        i1, j1, i2, j2 = 1.46202, 34.72808, 17.48111, 46.11693
        d1, d2 = 19.1887, 19.65495
        self.assertAlmostEqual(get_distance((x1, y1), (x2, y2)), d1, places=4)
        self.assertAlmostEqual(get_distance((i1, j1), (i2, j2)), d2, places=4)

#    def test_arrange_by_position(self):


if __name__ == '__main__':
    unittest.main()
