import unittest
from player import *


class TestPlayer(unittest.TestCase):

    p = Player('blue', (25, 25), (100, 100), 0, 3)

    def test_find_movement_direction(self):
        counter_clockwise = [
            (1, 0),
            (89, 0),
            (90, 0),
            (91, 0),
            (179, 0),
            (0, 181),
            (0, 269),
            (0, 270),
            (0, 271),
            (0, 328.99999999999903),
            (0, 359)
        ]
        clockwise = [
            (0, 0),
            (0, 360),
            (0, 1),
            (0, 31.000000000000977),
            (0, 89),
            (0, 90),
            (0, 91),
            (0, 179),
            (181, 0),
            (269, 0),
            (270, 0),
            (271, 0),
            (359, 0)
        ]
        for i in counter_clockwise:
            d = self.p.find_movement_direction(i[0], i[1])
            self.assertEqual(d, -1.0, msg="Origin=%s, Dest=%s (%s != -1.0)" % (i[0], i[1], d))
        for i in clockwise:
            d = self.p.find_movement_direction(i[0], i[1])
            self.assertEqual(d, 1.0, msg="Origin=%s, Dest=%s, (%s != 1.0)" % (i[0], i[1], d))

    def test_governator(self):
        def test_same_same(governator_x, governator_y, left_stick_x, left_stick_y, msg):
            x, y = self.p.governator(governator_x, governator_y, left_stick_x, left_stick_y)
            self.assertEqual(left_stick_x, x, "%s (x): %s != %s" % (msg, left_stick_x, x))
            self.assertEqual(left_stick_y, y, "%s (y): %s != %s" % (msg, left_stick_y, y))

        def test_governed(governator_x, governator_y, left_stick_x, left_stick_y, asserted_x, asserted_y, msg):
            x, y = self.p.governator(governator_x, governator_y, left_stick_x, left_stick_y)
            self.assertAlmostEqual(asserted_x, x, msg="%s (x): %s != %s" % (msg, asserted_x, x))
            self.assertAlmostEqual(asserted_y, y, msg="%s (y): %s != %s" % (msg, asserted_y, y))

        # Test non-regulated cases (same same)
        # 0 degrees
        test_same_same(0, 1, 0, 1, '0 degree test')
        test_same_same(1, 0, 1, 0, '0 degree test')
        # 15 degrees
        test_same_same(500, 0, 0.96592582628907, 0.25881904510252, '15 degree test')
        test_same_same(500, 0, 0.96592582628907, -0.25881904510252, '-15 degree test')
        # 29 degrees
        test_same_same(1, 0, 0.8746197071394, 0.48480962024634, '29 degree test')
        test_same_same(1, 0, 0.8746197071394, -0.48480962024634, '-29 degree test')
        # Test regulated cases
        # 31 degrees
        test_governed(self.p.movement_speed, 0, 2.5715019021063, 1.5451142247302,
                      2.5715019021063, 1.5451142247302, '31 degree test')
        test_governed(self.p.movement_speed, 0, 2.5715019021063, -1.5451142247302,
                      2.5715019021063, -1.5451142247302, '-31 degree test')

if __name__ == '__main__':
    unittest.main()

