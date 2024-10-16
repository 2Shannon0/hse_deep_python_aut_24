import unittest
from lru_cache import LRUCache


class TestLRUCache(unittest.TestCase):
    def test1_set(self):
        cache = LRUCache(2)
        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertEqual(cache.cache["k1"].value, "val1")
        self.assertEqual(cache.cache["k2"].value, "val2")

    def test2_overflow(self):
        cache = LRUCache(0)
        cache.set("k1", "val1")
        self.assertEqual(cache['k1'], None)

        cache = LRUCache(2)
        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k3", "val3")

        self.assertEqual(cache['k1'], None)
        self.assertEqual(cache['k2'], "val2")
        self.assertEqual(cache['k3'], "val3")

    def test3_overall(self):
        cache = LRUCache(2)
        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertEqual(cache['k3'], None)
        self.assertEqual(cache['k2'], 'val2')
        self.assertEqual(cache.get('k1'), 'val1')

        cache.set("k3", "val3")

        self.assertEqual(cache['k3'], "val3")
        self.assertEqual(cache['k2'], None)
        self.assertEqual(cache.get('k1'), 'val1')

    def test4_update_value(self):
        cache = LRUCache(2)
        cache.set("k1", "val1")
        self.assertEqual(cache.get('k1'), 'val1')
        cache.set("k2", "val2")
        cache.set("k1", "new_val1")

        self.assertEqual(cache.get("k1"), "new_val1")
        self.assertEqual(cache.get("k2"), "val2")
