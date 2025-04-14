import unittest
from custom_class import CustomList
# pylint: disable=too-many-public-methods, pointless-statement


class TestCustomList(unittest.TestCase):

    def test_add_two_custom_lists_equal_length(self):
        list1 = CustomList([1, 2, 3])
        list2 = CustomList([1, 2, 3, 4])
        result = list1 + list2
        self.assertEqual(list(result), [2, 4, 6, 4])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(list1), [1, 2, 3])
        self.assertEqual(list(list2), [1, 2, 3, 4])

    def test_add_two_custom_lists_different_length(self):
        list1 = CustomList([1, 2, 3])
        list2 = CustomList([4, 5])
        result1 = list1 + list2
        result2 = list2 + list1
        self.assertEqual(list(result1), [5, 7, 3])
        self.assertIsInstance(result1, CustomList)
        self.assertEqual(list(result2), [5, 7, 3])
        self.assertIsInstance(result2, CustomList)
        self.assertEqual(list(list1), [1, 2, 3])
        self.assertEqual(list(list2), [4, 5])

    def test_add_custom_list_and_regular_list(self):
        list1 = CustomList([1, 2, 3])
        regular_list1 = [4, 5]
        regular_list2 = [1, 2, 3, 4]
        result1 = list1 + regular_list1
        result2 = list1 + regular_list2
        self.assertEqual(list(result1), [5, 7, 3])
        self.assertIsInstance(result1, CustomList)
        self.assertEqual(list(result2), [2, 4, 6, 4])
        self.assertIsInstance(result2, CustomList)
        self.assertEqual(list(list1), [1, 2, 3])

    def test_add_custom_list_and_integer(self):
        list1 = CustomList([1, 2, 3])
        result = list1 + 5
        self.assertEqual(list(result), [6, 7, 8])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(list1), [1, 2, 3])

    def test_add_empty_lists(self):
        empty = CustomList()
        result = empty + empty
        self.assertEqual(list(result), [])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(empty), [])

    def test_add_with_empty_list(self):
        empty = CustomList()
        list1 = CustomList([1, 2, 3])
        result = list1 + empty
        self.assertEqual(list(result), [1, 2, 3])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(list1), [1, 2, 3])
        self.assertEqual(list(empty), [])

    def test_add_unsupported_type(self):
        list1 = CustomList([1, 2, 3])
        with self.assertRaises(TypeError):
            list1 + "string"
        self.assertEqual(list(list1), [1, 2, 3])

    def test_radd_regular_list_and_custom_list(self):
        list1 = CustomList([4, 5])
        regular_list1 = [1, 2, 3]
        regular_list2 = [7]
        result1 = regular_list1 + list1
        result2 = regular_list2 + list1
        self.assertEqual(list(result1), [5, 7, 3])
        self.assertIsInstance(result1, CustomList)
        self.assertEqual(list(result2), [11, 5])
        self.assertIsInstance(result2, CustomList)
        self.assertEqual(list(list1), [4, 5])

    def test_radd_integer_and_custom_list(self):
        list1 = CustomList([1, 2, 3])
        result = 5 + list1
        self.assertEqual(list(result), [6, 7, 8])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(list1), [1, 2, 3])

    def test_radd_unsupported_type(self):
        list1 = CustomList([1, 2, 3])
        with self.assertRaises(TypeError):
            "string" + list1
        self.assertEqual(list(list1), [1, 2, 3])

    def test_sub_two_custom_lists_equal_length(self):
        list1 = CustomList([1, 2, 3])
        list2 = CustomList([2, 4, 6])
        result1 = list1 - list2
        result2 = list2 - list1
        self.assertEqual(list(result1), [-1, -2, -3])
        self.assertIsInstance(result1, CustomList)
        self.assertEqual(list(result2), [1, 2, 3])
        self.assertIsInstance(result2, CustomList)
        self.assertEqual(list(list1), [1, 2, 3])
        self.assertEqual(list(list2), [2, 4, 6])

    def test_sub_two_custom_lists_different_length(self):
        list1 = CustomList([1, 2, 3])
        list2 = CustomList([1, 2, 3, 4])
        result1 = list1 - list2
        result2 = list2 - list1
        self.assertEqual(list(result1), [0, 0, 0, -4])
        self.assertIsInstance(result1, CustomList)
        self.assertEqual(list(result2), [0, 0, 0, 4])
        self.assertIsInstance(result2, CustomList)
        self.assertEqual(list(list1), [1, 2, 3])
        self.assertEqual(list(list2), [1, 2, 3, 4])

    def test_sub_custom_list_and_regular_list(self):
        list1 = CustomList([1, 2, 3])
        regular_list1 = [4, 5]
        regular_list2 = [2, 3, 4, 5]
        result1 = list1 - regular_list1
        result2 = list1 - regular_list2
        self.assertEqual(list(result1), [-3, -3, 3])
        self.assertIsInstance(result1, CustomList)
        self.assertEqual(list(result2), [-1, -1, -1, -5])
        self.assertEqual(list(list1), [1, 2, 3])

    def test_sub_custom_list_and_integer(self):
        list1 = CustomList([1, 2, 3])
        result = list1 - 1
        self.assertEqual(list(result), [0, 1, 2])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(list1), [1, 2, 3])

    def test_sub_empty_lists(self):
        empty = CustomList()
        result = empty - empty
        self.assertEqual(list(result), [])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(empty), [])

    def test_sub_with_empty_list(self):
        empty = CustomList()
        list1 = CustomList([1, 2, 3])
        result = list1 - empty
        self.assertEqual(list(result), [1, 2, 3])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(list1), [1, 2, 3])
        self.assertEqual(list(empty), [])

    def test_sub_unsupported_type(self):
        list1 = CustomList([1, 2, 3])
        with self.assertRaises(TypeError):
            list1 - "string"
        self.assertEqual(list(list1), [1, 2, 3])

    def test_rsub_regular_list_and_custom_list(self):
        list1 = CustomList([4, 5])
        regular_list1 = [1, 2, 3]
        regular_list2 = [7]
        result1 = regular_list1 - list1
        result2 = regular_list2 - list1
        self.assertEqual(list(result1), [-3, -3, 3])
        self.assertIsInstance(result1, CustomList)
        self.assertEqual(list(result2), [3, -5])
        self.assertIsInstance(result2, CustomList)
        self.assertEqual(list(list1), [4, 5])

    def test_rsub_integer_and_custom_list(self):
        list1 = CustomList([1, 2, 3])
        result = 5 - list1
        self.assertEqual(list(result), [4, 3, 2])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(list1), [1, 2, 3])

    def test_rsub_unsupported_type(self):
        list1 = CustomList([1, 2, 3])
        with self.assertRaises(TypeError):
            "string" - list1
        self.assertEqual(list(list1), [1, 2, 3])

    def test_eq_true(self):
        self.assertTrue(CustomList([1, 2, 3]) == CustomList([6]))
        self.assertTrue(CustomList([1, 2, 3]) == CustomList([1, 1, 1, 3]))

    def test_eq_false(self):
        self.assertFalse(CustomList([1, 2, 3]) == CustomList([7]))
        self.assertFalse(CustomList([1, 2, 3]) == CustomList([1, 1, 1, 4]))

    def test_eq_unsupported_type(self):
        list1 = CustomList([1, 2, 3])
        with self.assertRaises(TypeError):
            list1 == [1, 2, 3]

    def test_ne_unsupported_type(self):
        list1 = CustomList([1, 2, 3])
        with self.assertRaises(TypeError):
            list1 != [1, 2, 3]

    def test_lt_unsupported_type(self):
        list1 = CustomList([1, 2, 3])
        with self.assertRaises(TypeError):
            list1 < [1, 2, 3]

    def test_le_unsupported_type(self):
        list1 = CustomList([1, 2, 3])
        with self.assertRaises(TypeError):
            list1 <= [1, 2, 3]

    def test_gt_unsupported_type(self):
        list1 = CustomList([1, 2, 3])
        with self.assertRaises(TypeError):
            list1 > [1, 2, 3]

    def test_ge_unsupported_type(self):
        list1 = CustomList([1, 2, 3])
        with self.assertRaises(TypeError):
            list1 >= [1, 2, 3]

    def test_ne_true(self):
        self.assertTrue(CustomList([1, 2, 3]) != CustomList([7]))
        self.assertTrue(CustomList([1, 2, 3]) != CustomList([1, 1, 1, 4]))

    def test_ne_false(self):
        self.assertFalse(CustomList([1, 2, 3]) != CustomList([6]))
        self.assertFalse(CustomList([1, 2, 3]) != CustomList([1, 1, 1, 3]))

    def test_lt_true(self):
        self.assertTrue(CustomList([1, 2, 3]) < CustomList([7]))
        self.assertTrue(CustomList([1, 2, 3]) < CustomList([1, 1, 1, 4]))

    def test_lt_false(self):
        self.assertFalse(CustomList([1, 2, 3]) < CustomList([6]))
        self.assertFalse(CustomList([1, 2, 3]) < CustomList([1, 1, 1, 3]))

    def test_le_true(self):
        self.assertTrue(CustomList([1, 2, 3]) <= CustomList([6]))
        self.assertTrue(CustomList([1, 2, 3]) <= CustomList([7]))
        self.assertTrue(CustomList([1, 2, 3]) <= CustomList([1, 1, 1, 3]))

    def test_le_false(self):
        self.assertFalse(CustomList([1, 2, 3]) <= CustomList([5]))
        self.assertFalse(CustomList([1, 2, 3]) <= CustomList([1, 1, 1, 2]))

    def test_gt_true(self):
        self.assertTrue(CustomList([1, 2, 3]) > CustomList([5]))
        self.assertTrue(CustomList([1, 2, 3]) > CustomList([1, 1, 1, 2]))

    def test_gt_false(self):
        self.assertFalse(CustomList([1, 2, 3]) > CustomList([6]))
        self.assertFalse(CustomList([1, 2, 3]) > CustomList([1, 1, 1, 3]))

    def test_ge_true(self):
        self.assertTrue(CustomList([1, 2, 3]) >= CustomList([6]))
        self.assertTrue(CustomList([1, 2, 3]) >= CustomList([5]))
        self.assertTrue(CustomList([1, 2, 3]) >= CustomList([1, 1, 1, 3]))

    def test_ge_false(self):
        self.assertFalse(CustomList([1, 2, 3]) >= CustomList([7]))
        self.assertFalse(CustomList([1, 2, 3]) >= CustomList([1, 1, 1, 4]))

    def test_str_empty_list(self):
        empty = CustomList()
        self.assertEqual(str(empty), "CustomList([]), sum: 0")

    def test_str_non_empty_list(self):
        list1 = CustomList([1, 2, 3])
        list2 = CustomList([4, 5])
        self.assertEqual(str(list1), "CustomList([1, 2, 3]), sum: 6")
        self.assertEqual(str(list2), "CustomList([4, 5]), sum: 9")

    def test_single_element_list_operations(self):
        single = CustomList([5])
        self.assertEqual(list(single + single), [10])
        self.assertEqual(list(single - single), [0])
        self.assertEqual(list(single + 5), [10])
        self.assertEqual(list(5 + single), [10])
        self.assertEqual(list(single - 2), [3])
        self.assertEqual(list(10 - single), [5])
        self.assertEqual(list(single), [5])

    def test_operations_with_negative_numbers(self):
        list1 = CustomList([1, 2, 3])
        neg_list = CustomList([-1, -2, -3])
        self.assertEqual(list(neg_list + list1), [0, 0, 0])
        self.assertEqual(list(neg_list - list1), [-2, -4, -6])
        self.assertEqual(list(neg_list + (-5)), [-6, -7, -8])
        self.assertEqual(list(neg_list - (-1)), [0, -1, -2])
        self.assertEqual(list(list1), [1, 2, 3])
        self.assertEqual(list(neg_list), [-1, -2, -3])
