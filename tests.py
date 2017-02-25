import unittest
from segmenter import time_difference


class TestSegmenterFunctions(unittest.TestCase):

    def test_time_difference(self):
        self.assertEqual(time_difference("11:34", "11:34"), 0)
        self.assertEqual(time_difference("12:00", "11:59"), 1)
        self.assertEqual(time_difference("06:00", "4:30"), 90)
        self.assertRaises(Exception, time_difference, "4:30", "6:00")


if __name__ == '__main__':
    unittest.main()
