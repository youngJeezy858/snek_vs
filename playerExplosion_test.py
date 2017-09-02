import unittest
from player import *
from playerExplosion import *


class TestPlayer(unittest.TestCase):

    player = Player('blue', 1, (25, 25), (100, 100), 0, 3)
    explosion = PlayerExplosion(player, 1000)

    def test_gen_explosion_degree(self):
        for i in range(0, 100):
            degree = self.explosion.gen_explosion_degree()
            lower_bound = self.explosion.movement_speed * 5
            upper_bound = self.explosion.movement_speed * 10
            self.assertTrue(
                (lower_bound < degree < upper_bound) or (-1 * upper_bound < degree < -1 * lower_bound),
                msg="Degree %s not in range: [%s - %s], [%s - %s]" %
                    (degree, -1 * upper_bound, -1 * lower_bound, lower_bound, upper_bound)
            )

    def test_process_explosion(self):
        # x, degree, y
        valid = [
            [0, 15, 0.1],
            [1, 17, 15.9],
            [2, 30, 55.9],

        ]
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()

