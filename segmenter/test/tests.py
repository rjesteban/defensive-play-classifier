import unittest
import json
from segmenter.core import convert_moment_to_action
from segmenter.utils import time_difference, all_on_one_side, within_the_paint
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

    def test_within_the_paint(self):
        eid = 74
        moment = get_moment(testdata, eid)
        outside = within_the_paint(moment[223][5][0], eid)
        msg = moment[223][5][0]
        self.assertFalse(outside, msg=msg)
        msg = moment[332][5][0]
        inside = within_the_paint(moment[332][5][0], eid)
        self.assertTrue(inside, msg=msg)


class TestSegmenterCoreFunctions(unittest.TestCase):

    def test_convert_moment_to_action(self):
        eid = 4
        action = convert_moment_to_action(testdata, eid)
        frames = len(action.coords)
        msg = "length is: " + str(frames)
        self.assertTrue(309 <= frames <= 349, msg=msg)


if __name__ == '__main__':
    unittest.main()
