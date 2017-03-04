from action.core import load_action
from preprocessor.utils import get_distance, arrange_by_position
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

    def test_arrange_by_position(self):
        action = load_action("0021500582", 4)

        off = str([[203500, u'C', u'home', 1], [201586, u'F', u'home', 1],
                  [201142, u'F', u'home', 1], [201566, u'G', u'home', 1],
                  [203460, u'G', u'home', 1]])

        deff = str([[201580, u'C', u'visitor', 1],
                   [101111, u'F', u'visitor', 1],
                   [202379, u'F', u'visitor', 1],
                   [101109, u'G', u'visitor', 1],
                   [200826, u'G', u'visitor', 1]])

        self.assertEquals(str(arrange_by_position(action).offense), off)
        self.assertEquals(str(arrange_by_position(action).defense), deff)


if __name__ == '__main__':
    unittest.main()
