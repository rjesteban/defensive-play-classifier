import unittest
import json
from segmenter.utils import time_difference, all_on_one_side
from sportvu.utils import get_moment

testdata = json.load(open('data/sportvu/0021500582.json'))


class TestSegmenterUtilFunctions(unittest.TestCase):

    def test_time_difference(self):
        self.assertEqual(time_difference("11:34", "11:34"), 0)
        self.assertEqual(time_difference("12:00", "11:59"), 1)
        self.assertEqual(time_difference("06:00", "4:30"), 90)
        self.assertRaises(Exception, time_difference, "4:30", "6:00")

    def test_all_on_one_side(self):
        eid, frame70, frame268 = 4, 70, 268
        moment = get_moment(testdata, eid)
        self.assertFalse(all_on_one_side(moment, eid, frame70))
        self.assertTrue(all_on_one_side(moment, eid, frame268))


if __name__ == '__main__':
    unittest.main()
