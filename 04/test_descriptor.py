import unittest
from descriptor import Data, String, Integer, PositiveInteger
# pylint: disable=too-few-public-methods
# pylint: disable=invalid-name


class TestIntegerDescriptor(unittest.TestCase):
    def setUp(self):
        class TestClass:
            value = Integer()
        self.TestClass = TestClass
        self.obj1 = TestClass()
        self.obj2 = TestClass()

    def test_integer_accepts_valid_int(self):
        self.obj1.value = 10
        self.assertEqual(self.obj1.value, 10)
        self.assertIsNone(self.obj2.value)

    def test_integer_rejects_non_int(self):
        self.obj1.value = 5
        with self.assertRaisesRegex(TypeError, r"Значение 3.14 должно быть int, а не float"):
            self.obj1.value = 3.14
        self.assertEqual(self.obj1.value, 5)

        with self.assertRaisesRegex(TypeError, r"Значение hello должно быть int, а не str"):
            self.obj1.value = "hello"
        self.assertEqual(self.obj1.value, 5)

    def test_descriptor_get_from_class(self):
        descriptor = self.TestClass.value
        self.assertIsInstance(descriptor, Integer)


class TestStringDescriptor(unittest.TestCase):
    def setUp(self):
        class TestClass:
            value = String()
        self.TestClass = TestClass
        self.obj1 = TestClass()
        self.obj2 = TestClass()

    def test_string_accepts_valid_str(self):
        self.obj1.value = "Test"
        self.assertEqual(self.obj1.value, "Test")
        self.assertIsNone(self.obj2.value)

    def test_string_rejects_non_string(self):
        self.obj1.value = "Initial"
        with self.assertRaisesRegex(TypeError, r"Значение 123 должно быть str, а не int"):
            self.obj1.value = 123
        self.assertEqual(self.obj1.value, "Initial")

    def test_descriptor_get_from_class(self):
        descriptor = type(self.obj1).value
        self.assertIsInstance(descriptor, String)


class TestPositiveIntegerDescriptor(unittest.TestCase):
    def setUp(self):
        class TestClass:
            value = PositiveInteger()
        self.TestClass = TestClass
        self.obj1 = TestClass()
        self.obj2 = TestClass()

    def test_positive_integer_accepts_valid_value(self):
        self.obj1.value = 1
        self.assertEqual(self.obj1.value, 1)
        self.assertIsNone(self.obj2.value)

    def test_positive_integer_rejects_invalid_values(self):
        self.obj1.value = 10
        with self.assertRaisesRegex(ValueError, r"Значение -1 должно быть положительным"):
            self.obj1.value = -1
        self.assertEqual(self.obj1.value, 10)

        with self.assertRaisesRegex(ValueError, r"Значение 0 должно быть положительным"):
            self.obj1.value = 0
        self.assertEqual(self.obj1.value, 10)

        with self.assertRaisesRegex(TypeError, r"Значение 3.14 должно быть int"):
            self.obj1.value = 3.14
        self.assertEqual(self.obj1.value, 10)

    def test_descriptor_get_from_class(self):
        descriptor = type(self.obj1).value
        self.assertIsInstance(descriptor, PositiveInteger)


class TestDataClass(unittest.TestCase):
    def setUp(self):
        self.valid_data = {"num": 10, "name": "Python", "price": 100}

    def test_valid_initialization(self):
        data = Data(**self.valid_data)
        self.assertEqual(data.num, 10)
        self.assertEqual(data.name, "Python")
        self.assertEqual(data.price, 100)

    def test_invalid_initialization(self):
        test_cases = [
            ("num", "not an int", TypeError, "должно быть int"),
            ("name", 999, TypeError, "должно быть str"),
            ("price", -50, ValueError, "должно быть положительным"),
            ("price", 0, ValueError, "должно быть положительным")
        ]

        for field, value, exc_type, err_msg in test_cases:
            with self.subTest(field=field, value=value):
                test_data = self.valid_data.copy()
                test_data[field] = value
                with self.assertRaisesRegex(exc_type, err_msg):
                    Data(**test_data)

    def test_field_isolation(self):
        data1 = Data(**self.valid_data)
        data2 = Data(**self.valid_data)

        data1.num = 20
        self.assertEqual(data1.num, 20)
        self.assertEqual(data2.num, 10)

    def test_invalid_updates(self):
        data = Data(**self.valid_data)
        original_values = {"num": data.num, "name": data.name, "price": data.price}

        test_cases = [
            ("num", "123", TypeError),
            ("name", 123, TypeError),
            ("price", -1, ValueError)
        ]

        for field, value, exc_type in test_cases:
            with self.subTest(field=field, value=value):
                with self.assertRaises(exc_type):
                    setattr(data, field, value)
                self.assertEqual(getattr(data, field), original_values[field])
