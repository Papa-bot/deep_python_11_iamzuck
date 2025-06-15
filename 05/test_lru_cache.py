import unittest
from lru_cache import LRUCache


class TestLRUCache(unittest.TestCase):
    def test_initialization(self):
        with self.assertRaises(ValueError):
            LRUCache(0)
        with self.assertRaises(ValueError):
            LRUCache(-5)

    def test_basic_set_get(self):
        cache = LRUCache(3)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)
        self.assertEqual(cache.get("a"), 1)
        self.assertEqual(cache.get("b"), 2)
        self.assertEqual(cache.get("c"), 3)
        self.assertIsNone(cache.get("d"))

    def test_limit_enforcement(self):
        cache = LRUCache(3)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)
        cache.set("d", 4)
        self.assertIsNone(cache.get("a"))
        self.assertEqual(cache.get("b"), 2)
        self.assertEqual(cache.get("c"), 3)
        self.assertEqual(cache.get("d"), 4)

    def test_lru_order(self):
        cache = LRUCache(3)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)
        cache.get("a")
        cache.set("d", 4)
        self.assertIsNone(cache.get("b"))
        self.assertEqual(cache.get("a"), 1)
        self.assertEqual(cache.get("c"), 3)
        self.assertEqual(cache.get("a"), 1)

    def test_dict_syntax(self):
        cache = LRUCache(3)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)
        cache["f"] = 6
        self.assertEqual(cache["f"], 6)
        self.assertIsNone(cache.get("a"))
        self.assertEqual(cache.get("b"), 2)
        self.assertEqual(cache.get("c"), 3)
        self.assertIsNone(cache["missing_key"])

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

    def test_update_existing_key(self):
        cache = LRUCache(3)
        cache.set('x', 10)
        cache.set('y', 20)
        cache.set('z', 30)
        cache.set('x', 40)
        cache.set('w', 50)
        self.assertIsNone(cache.get('y'))
        self.assertEqual(cache.get('x'), 40)
        self.assertEqual(cache.get('z'), 30)
        self.assertEqual(cache.get('w'), 50)
