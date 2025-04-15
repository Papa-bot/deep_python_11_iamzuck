import unittest
from descriptor import Data, String, Integer, PositiveInteger
# pylint: disable=too-few-public-methods


class TestIntegerDescriptor(unittest.TestCase):
    def setUp(self):
        class TestClass:
            value = Integer()
        self.test_obj = TestClass()

    def test_integer_accepts_valid_int(self):
        self.test_obj.value = 10
        self.assertEqual(self.test_obj.value, 10)

    def test_integer_rejects_non_int(self):
        with self.assertRaises(TypeError):
            self.test_obj.value = 3.14
        with self.assertRaises(TypeError):
            self.test_obj.value = "hello"
        with self.assertRaises(TypeError):
            self.test_obj.value = None

    def test_descriptor_get_from_class(self):
        descriptor = type(self.test_obj).value
        self.assertIsInstance(descriptor, Integer)


class TestStringDescriptor(unittest.TestCase):
    def setUp(self):
        class TestClass:
            value = String()
        self.test_obj = TestClass()

    def test_string_accepts_valid_str(self):
        self.test_obj.value = "TestString"
        self.assertEqual(self.test_obj.value, "TestString")

    def test_string_rejects_non_string(self):
        with self.assertRaises(TypeError):
            self.test_obj.value = 123
        with self.assertRaises(TypeError):
            self.test_obj.value = 3.14
        with self.assertRaises(TypeError):
            self.test_obj.value = True

    def test_descriptor_get_from_class(self):
        descriptor = type(self.test_obj).value
        self.assertIsInstance(descriptor, String)


class TestPositiveIntegerDescriptor(unittest.TestCase):
    def setUp(self):
        class TestClass:
            value = PositiveInteger()
        self.test_obj = TestClass()

    def test_positive_integer_accepts_valid_value(self):
        self.test_obj.value = 1
        self.assertEqual(self.test_obj.value, 1)
        self.test_obj.value = 100
        self.assertEqual(self.test_obj.value, 100)

    def test_positive_integer_rejects_zero(self):
        with self.assertRaises(ValueError):
            self.test_obj.value = 0

    def test_positive_integer_rejects_negative(self):
        with self.assertRaises(ValueError):
            self.test_obj.value = -1
        with self.assertRaises(ValueError):
            self.test_obj.value = -100

    def test_positive_integer_rejects_non_int(self):
        with self.assertRaises(TypeError):
            self.test_obj.value = 3.14
        with self.assertRaises(TypeError):
            self.test_obj.value = "string"

    def test_descriptor_get_from_class(self):
        descriptor = type(self.test_obj).value
        self.assertIsInstance(descriptor, PositiveInteger)


class TestDataClass(unittest.TestCase):
    def test_data_initialization(self):
        data = Data(num=10, name="Python", price=100)
        self.assertEqual(data.num, 10)
        self.assertEqual(data.name, "Python")
        self.assertEqual(data.price, 100)

    def test_data_invalid_num_type(self):
        """Проверяем, что при неверном типе num вылетит TypeError."""
        with self.assertRaises(TypeError):
            Data(num="not an int", name="Python", price=100)

    def test_data_invalid_name_type(self):
        """Проверяем, что при неверном типе name вылетит TypeError."""
        with self.assertRaises(TypeError):
            Data(num=10, name=999, price=100)

    def test_data_invalid_price_negative(self):
        """Проверяем, что при отрицательном значении price вылетит ValueError."""
        with self.assertRaises(ValueError):
            Data(num=10, name="Python", price=-50)

    def test_data_invalid_price_zero(self):
        """Проверяем, что при значении price = 0 вылетит ValueError."""
        with self.assertRaises(ValueError):
            Data(num=10, name="Python", price=0)

    def test_setters_after_init(self):
        """Проверяем, что можно корректно переустанавливать значения
           в объекте Data и срабатывают все проверки."""
        data = Data(num=1, name="Test", price=10)

        data.num = 20
        self.assertEqual(data.num, 20)

        data.name = "NewName"
        self.assertEqual(data.name, "NewName")

        data.price = 30
        self.assertEqual(data.price, 30)

        with self.assertRaises(TypeError):
            data.num = "123"
        with self.assertRaises(TypeError):
            data.name = 123
        with self.assertRaises(ValueError):
            data.price = -1
