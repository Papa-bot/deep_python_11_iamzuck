import unittest
from custom_class import CustomList
# pylint: disable=too-many-public-methods, pointless-statement


class TestCustomList(unittest.TestCase):
    def setUp(self):
        self.empty = CustomList()
        self.single = CustomList([5])
        self.list1 = CustomList([1, 2, 3])
        self.list2 = CustomList([4, 5])
        self.list3 = CustomList([1, 2, 3, 4])
        self.regular_list1 = [1, 2, 3]
        self.regular_list2 = [4, 5]

    def test_add_two_custom_lists_equal_length(self):
        result = self.list1 + self.list3
        self.assertEqual(result, CustomList([2, 4, 6, 4]))
        self.assertIsInstance(result, CustomList)

    def test_add_two_custom_lists_different_length(self):
        result = self.list1 + self.list2
        self.assertEqual(result, CustomList([5, 7, 3]))
        self.assertIsInstance(result, CustomList)

    def test_add_custom_list_and_regular_list(self):
        result = self.list1 + self.regular_list2
        self.assertEqual(result, CustomList([5, 7, 3]))
        self.assertIsInstance(result, CustomList)

    def test_add_custom_list_and_integer(self):
        result = self.list1 + 5
        self.assertEqual(result, CustomList([6, 7, 8]))
        self.assertIsInstance(result, CustomList)

    def test_add_empty_lists(self):
        result = self.empty + self.empty
        self.assertEqual(result, CustomList([]))
        self.assertIsInstance(result, CustomList)

    def test_add_with_empty_list(self):
        result = self.list1 + self.empty
        self.assertEqual(result, CustomList([1, 2, 3]))
        self.assertIsInstance(result, CustomList)

    def test_add_unsupported_type(self):
        with self.assertRaises(TypeError):
            self.list1 + "string"

    def test_radd_regular_list_and_custom_list(self):
        result = self.regular_list1 + self.list2
        self.assertEqual(result, CustomList([5, 7, 3]))
        self.assertIsInstance(result, CustomList)

    def test_radd_integer_and_custom_list(self):
        result = 5 + self.list1
        self.assertEqual(result, CustomList([6, 7, 8]))
        self.assertIsInstance(result, CustomList)

    def test_radd_unsupported_type(self):
        with self.assertRaises(TypeError):
            "string" + self.list1

    def test_sub_two_custom_lists_equal_length(self):
        result = self.list1 - self.list3
        self.assertEqual(result, CustomList([0, 0, 0, -4]))
        self.assertIsInstance(result, CustomList)

    def test_sub_two_custom_lists_different_length(self):
        result = self.list1 - self.list2
        self.assertEqual(result, CustomList([-3, -3, 3]))
        self.assertIsInstance(result, CustomList)

    def test_sub_custom_list_and_regular_list(self):
        result = self.list1 - self.regular_list2
        self.assertEqual(result, CustomList([-3, -3, 3]))
        self.assertIsInstance(result, CustomList)

    def test_sub_custom_list_and_integer(self):
        result = self.list1 - 1
        self.assertEqual(result, CustomList([0, 1, 2]))
        self.assertIsInstance(result, CustomList)

    def test_sub_empty_lists(self):
        result = self.empty - self.empty
        self.assertEqual(result, CustomList([]))
        self.assertIsInstance(result, CustomList)

    def test_sub_with_empty_list(self):
        result = self.list1 - self.empty
        self.assertEqual(result, CustomList([1, 2, 3]))
        self.assertIsInstance(result, CustomList)

    def test_sub_unsupported_type(self):
        with self.assertRaises(TypeError):
            self.list1 - "string"

    def test_rsub_regular_list_and_custom_list(self):
        result = self.regular_list1 - self.list2
        self.assertEqual(result, CustomList([-3, -3, 3]))
        self.assertIsInstance(result, CustomList)

    def test_rsub_integer_and_custom_list(self):
        result = 5 - self.list1
        self.assertEqual(result, CustomList([4, 3, 2]))
        self.assertIsInstance(result, CustomList)

    def test_rsub_unsupported_type(self):
        with self.assertRaises(TypeError):
            "string" - self.list1

    def test_eq_true(self):
        self.assertTrue(CustomList([1, 2, 3]) == CustomList([6]))
        self.assertTrue(CustomList([1, 2, 3]) == CustomList([1, 1, 1, 3]))

    def test_eq_false(self):
        self.assertFalse(CustomList([1, 2, 3]) == CustomList([7]))
        self.assertFalse(CustomList([1, 2, 3]) == CustomList([1, 1, 1, 4]))

    def test_eq_unsupported_type(self):
        with self.assertRaises(TypeError):
            self.list1 == [1, 2, 3]

    def test_ne_unsupported_type(self):
        with self.assertRaises(TypeError):
            self.list1 != [1, 2, 3]

    def test_lt_unsupported_type(self):
        with self.assertRaises(TypeError):
            self.list1 < [1, 2, 3]

    def test_le_unsupported_type(self):
        with self.assertRaises(TypeError):
            self.list1 <= [1, 2, 3]

    def test_gt_unsupported_type(self):
        with self.assertRaises(TypeError):
            self.list1 > [1, 2, 3]

    def test_ge_unsupported_type(self):
        with self.assertRaises(TypeError):
            self.list1 >= [1, 2, 3]

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
        self.assertEqual(str(self.empty), "CustomList([]), sum: 0")

    def test_str_non_empty_list(self):
        self.assertEqual(str(self.list1), "CustomList([1, 2, 3]), sum: 6")
        self.assertEqual(str(self.list2), "CustomList([4, 5]), sum: 9")

    def test_original_lists_unchanged_after_add(self):
        original1 = CustomList([1, 2, 3])
        original2 = CustomList([4, 5])
        result = original1 + original2
        self.assertEqual(original1, CustomList([1, 2, 3]))
        self.assertEqual(original2, CustomList([4, 5]))
        self.assertEqual(result, CustomList([5, 7, 3]))

    def test_original_lists_unchanged_after_sub(self):
        original1 = CustomList([1, 2, 3])
        original2 = CustomList([4, 5])
        result = original1 - original2
        self.assertEqual(original1, CustomList([1, 2, 3]))
        self.assertEqual(original2, CustomList([4, 5]))
        self.assertEqual(result, CustomList([-3, -3, 3]))

    def test_single_element_list_operations(self):
        self.assertEqual(self.single + self.single, CustomList([10]))
        self.assertEqual(self.single - self.single, CustomList([0]))
        self.assertEqual(self.single + 5, CustomList([10]))
        self.assertEqual(5 + self.single, CustomList([10]))
        self.assertEqual(self.single - 2, CustomList([3]))
        self.assertEqual(10 - self.single, CustomList([5]))

    def test_operations_with_negative_numbers(self):
        neg_list = CustomList([-1, -2, -3])
        self.assertEqual(neg_list + self.list1, CustomList([0, 0, 0]))
        self.assertEqual(neg_list - self.list1, CustomList([-2, -4, -6]))
        self.assertEqual(neg_list + (-5), CustomList([-6, -7, -8]))
        self.assertEqual(neg_list - (-1), CustomList([0, -1, -2]))
