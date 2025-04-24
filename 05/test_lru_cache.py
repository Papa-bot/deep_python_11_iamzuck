import unittest
from lru_cache import LRUCache


class TestLRUCache(unittest.TestCase):
    def setUp(self):
        self.cache = LRUCache(3)
        self.cache.set("a", 1)
        self.cache.set("b", 2)
        self.cache.set("c", 3)

    def test_initialization(self):
        with self.assertRaises(ValueError):
            LRUCache(0)
        with self.assertRaises(ValueError):
            LRUCache(-5)

    def test_basic_set_get(self):
        self.assertEqual(self.cache.get("a"), 1)
        self.assertEqual(self.cache.get("b"), 2)
        self.assertEqual(self.cache.get("c"), 3)
        self.assertIsNone(self.cache.get("d"))

    def test_limit_enforcement(self):
        self.cache.set("d", 4)
        self.assertIsNone(self.cache.get("a"))
        self.assertEqual(self.cache.get("d"), 4)

    def test_lru_order(self):
        self.cache.get("a")
        self.cache.set("d", 4)
        self.assertIsNone(self.cache.get("b"))
        self.assertEqual(self.cache.get("a"), 1)

    def test_dict_syntax(self):
        self.cache["f"] = 6
        self.assertEqual(self.cache["f"], 6)
        self.assertIsNone(self.cache["missing_key"])

    def test_edge_case_limit_one(self):
        cache = LRUCache(1)
        cache.set("x", 10)
        self.assertEqual(cache.get("x"), 10)
        cache.set("y", 20)
        self.assertIsNone(cache.get("x"))
        self.assertEqual(cache.get("y"), 20)

    def test_all_combinations(self):
        cache = LRUCache(2)
        cache.set(1, 1)
        cache.set(2, 2)
        self.assertEqual(cache.get(1), 1)
        cache.set(3, 3)
        self.assertIsNone(cache.get(2))
        cache.set(4, 4)
        self.assertIsNone(cache.get(1))
        self.assertEqual(cache.get(3), 3)
        self.assertEqual(cache.get(4), 4)
