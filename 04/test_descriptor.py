import unittest
from descriptor import SwimmingStats


class TestSwimmingStats(unittest.TestCase):

    def test_distance(self):
        stats = SwimmingStats('Иван', 2, 100)
        self.assertEqual(stats.distance, 50)

    def test_speed(self):
        stats = SwimmingStats('Иван', 4, 120)
        self.assertEqual(stats.speed, (4 * 25) / 120)

    def test_speed_divide_by_zero(self):
        stats = SwimmingStats('Иван', 3, 0)
        self.assertEqual(stats.speed, 0)

    def test_pools_count_validation(self):
        with self.assertRaises(ValueError):
            SwimmingStats('Иван', -1, 100)

    def test_time_validation(self):
        with self.assertRaises(ValueError):
            SwimmingStats('Иван', 2, -30)

    def test_pool_length_validation(self):
        with self.assertRaises(ValueError):
            SwimmingStats('Иван', 2, 100, -25)

    def test_swimmer_name_validation(self):
        with self.assertRaises(ValueError):
            SwimmingStats('', 2, 100)
