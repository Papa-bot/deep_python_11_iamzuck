import unittest
from unittest.mock import Mock, call, patch
from param_decorator import retry_deco


class TestRetryDeco(unittest.TestCase):

    def test_success_first_try(self):
        mock = Mock(return_value=42)

        @retry_deco(retries=3)
        def wrapped():
            return mock()

        result = wrapped()
        self.assertEqual(result, 42)
        self.assertEqual(mock.call_count, 1)

    def test_retry_until_success(self):
        mock = Mock(side_effect=[Exception("fail"), Exception("fail again"), 100])

        @retry_deco(retries=3)
        def wrapped():
            return mock()

        result = wrapped()
        self.assertEqual(result, 100)
        self.assertEqual(mock.call_count, 3)

    def test_stop_on_expected_exception(self):
        mock = Mock(side_effect=ValueError("bad value"))

        @retry_deco(retries=5, expected_exceptions=[ValueError])
        def wrapped():
            return mock()

        result = wrapped()
        self.assertIsNone(result)
        self.assertEqual(mock.call_count, 1)

    def test_continue_on_unexpected_exception(self):
        mock = Mock(side_effect=[KeyError("unexpected"), KeyError("again"), 777])

        @retry_deco(retries=3, expected_exceptions=[ValueError])
        def wrapped():
            return mock()

        result = wrapped()
        self.assertEqual(result, 777)
        self.assertEqual(mock.call_count, 3)

    def test_args_and_kwargs_combination(self):
        mock = Mock(side_effect=lambda x, y=0: x + y)

        @retry_deco(retries=2)
        def wrapped(x, y=0):
            return mock(x, y=y)

        self.assertEqual(wrapped(1, y=2), 3)
        self.assertEqual(mock.call_args, call(1, y=2))

    def test_retries_equals_one(self):
        mock = Mock(side_effect=[Exception("fail"), 5])

        @retry_deco(retries=1)
        def wrapped():
            return mock()

        result = wrapped()
        self.assertIsNone(result)
        self.assertEqual(mock.call_count, 1)

    def test_expected_exception_is_none(self):
        mock = Mock(side_effect=[TypeError("fail"), 100])

        @retry_deco(retries=2, expected_exceptions=None)
        def wrapped():
            return mock()

        result = wrapped()
        self.assertEqual(result, 100)
        self.assertEqual(mock.call_count, 2)

    def test_only_kwargs(self):
        mock = Mock(side_effect=lambda *, x: x * 2)

        @retry_deco(retries=2)
        def wrapped(*, x):
            return mock(x=x)

        self.assertEqual(wrapped(x=5), 10)
        self.assertEqual(mock.call_count, 1)

    def test_print_called_expected_number_of_times(self):
        mock = Mock(side_effect=[Exception("fail"), 100])

        @retry_deco(retries=2)
        def wrapped():
            return mock()

        with patch("builtins.print") as mock_print:
            result = wrapped()

        self.assertEqual(result, 100)
        self.assertEqual(mock.call_count, 2)

        printed_messages = [call_arg[0][0] for call_arg in mock_print.call_args_list]

        self.assertIn('attempt = 1, exception = Exception', " ".join(printed_messages))
        self.assertIn('attempt = 2, result = 100', " ".join(printed_messages))

    def test_zero_retries(self):
        mock = Mock(return_value=123)

        @retry_deco(retries=0)
        def wrapped():
            return mock()

        result = wrapped()
        self.assertIsNone(result)
        self.assertEqual(mock.call_count, 0)

    def test_negative_retries(self):
        mock = Mock(return_value=999)

        @retry_deco(retries=-5)
        def wrapped():
            return mock()

        result = wrapped()
        self.assertIsNone(result)
        self.assertEqual(mock.call_count, 0)

    def test_invalid_retries_type(self):
        with self.assertRaises(TypeError):
            @retry_deco(retries="three")
            def wrapped():
                return 1
            wrapped()

    def test_all_attempts_fail_return_none(self):
        mock = Mock(side_effect=Exception("fail"))

        @retry_deco(retries=3)
        def wrapped():
            return mock()

        result = wrapped()
        # Ожидаем, что после 3 неудачных попыток функция вернёт None
        self.assertIsNone(result)
        self.assertEqual(mock.call_count, 3)

    def test_exception_with_args_and_kwargs(self):
        def faulty_func(x, y=0):
            raise RuntimeError("fail")

        mock = Mock(side_effect=faulty_func)

        @retry_deco(retries=1)
        def wrapped(x, y=0):
            return mock(x, y=y)

        result = wrapped(1, y=2)
        self.assertIsNone(result)
        self.assertEqual(mock.call_count, 1)

    def test_exception_with_only_kwargs(self):
        def faulty_func(*, x):
            raise RuntimeError("fail")

        mock = Mock(side_effect=faulty_func)

        @retry_deco(retries=1)
        def wrapped(*, x):
            return mock(x=x)

        result = wrapped(x=5)
        self.assertIsNone(result)
        self.assertEqual(mock.call_count, 1)
