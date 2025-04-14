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

    def test_stop_on_expected_exception_and_raise_it(self):
        mock = Mock(side_effect=ValueError("bad value"))

        @retry_deco(retries=5, expected_exceptions=[ValueError])
        def wrapped():
            return mock()

        with self.assertRaises(ValueError) as cm:
            wrapped()

        self.assertEqual(str(cm.exception), "bad value")
        self.assertEqual(mock.call_count, 5)

    def test_continue_on_unexpected_exception_and_raise_last_one(self):
        mock = Mock(side_effect=[KeyError("unexpected"), KeyError("again"), TypeError("final")])

        @retry_deco(retries=3, expected_exceptions=[ValueError])
        def wrapped():
            return mock()

        with self.assertRaises(TypeError) as cm:
            wrapped()

        self.assertEqual(str(cm.exception), "final")
        self.assertEqual(mock.call_count, 3)

    def test_args_and_kwargs_combination(self):
        mock = Mock(side_effect=lambda x, y=0: x + y)

        @retry_deco(retries=2)
        def wrapped(x, y=0):
            return mock(x, y=y)

        self.assertEqual(wrapped(1, y=2), 3)
        self.assertEqual(mock.call_args, call(1, y=2))

    def test_retries_equals_one_with_exception(self):
        mock = Mock(side_effect=Exception("fail"))

        @retry_deco(retries=1)
        def wrapped():
            return mock()

        with self.assertRaises(Exception) as cm:
            wrapped()

        self.assertEqual(str(cm.exception), "fail")
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

    def test_print_output_for_success_case(self):
        mock = Mock(side_effect=[Exception("fail"), 100])

        @retry_deco(retries=2)
        def wrapped():
            return mock()

        with patch("builtins.print") as mock_print:
            wrapped()

        expected_calls = [
            call('\nrun "wrapped" attempt = 1 exception = Exception'),
            call('\nrun "wrapped" attempt = 2 result = 100')
        ]
        mock_print.assert_has_calls(expected_calls)

    def test_print_output_for_failed_case(self):
        mock = Mock(side_effect=[Exception("fail1"), Exception("fail2")])

        @retry_deco(retries=2)
        def wrapped():
            return mock()

        with patch("builtins.print") as mock_print:
            with self.assertRaises(Exception):
                wrapped()

        expected_calls = [
            call('\nrun "wrapped" attempt = 1 exception = Exception'),
            call('\nrun "wrapped" attempt = 2 exception = Exception')
        ]
        mock_print.assert_has_calls(expected_calls)

    def test_print_output_with_args_and_kwargs(self):
        mock = Mock(return_value=42)

        @retry_deco(retries=2)
        def wrapped(a, b=0):
            return mock(a, b=b)

        with patch("builtins.print") as mock_print:
            wrapped(1, b=2)

        printed_message = mock_print.call_args[0][0]
        self.assertIn('positional args = (1,)', printed_message)
        self.assertIn('keyword kwargs = {\'b\': 2}', printed_message)
        self.assertIn('result = 42', printed_message)

    def test_zero_retries_raises_immediately(self):
        mock = Mock(side_effect=Exception("should not be called"))

        @retry_deco(retries=0)
        def wrapped():
            return mock()

        with self.assertRaises(Exception) as cm:
            wrapped()

        self.assertEqual(str(cm.exception), "Function not attempted (retries=0)")
        self.assertEqual(mock.call_count, 0)

    def test_negative_retries_raises_immediately(self):
        with self.assertRaises(ValueError) as cm:
            @retry_deco(retries=-5)
            def wrapped():
                pass
        self.assertEqual(str(cm.exception), "retries cannot be negative")

    def test_invalid_retries_type(self):
        with self.assertRaises(TypeError):
            @retry_deco(retries="three")
            def wrapped():
                return 1
            wrapped()

    def test_all_attempts_fail_raise_last_exception(self):
        mock = Mock(side_effect=[Exception("fail1"), Exception("fail2"), Exception("fail3")])

        @retry_deco(retries=3)
        def wrapped():
            return mock()

        with self.assertRaises(Exception) as cm:
            wrapped()

        self.assertEqual(str(cm.exception), "fail3")
        self.assertEqual(mock.call_count, 3)

    def test_exception_with_args_and_kwargs_raised_properly(self):
        def faulty_func(x, y=0):
            raise RuntimeError(f"fail with x={x} y={y}")

        mock = Mock(side_effect=faulty_func)

        @retry_deco(retries=1)
        def wrapped(x, y=0):
            return mock(x, y=y)

        with self.assertRaises(RuntimeError) as cm:
            wrapped(1, y=2)

        self.assertEqual(str(cm.exception), "fail with x=1 y=2")
        self.assertEqual(mock.call_count, 1)

    def test_exception_with_only_kwargs_raised_properly(self):
        def faulty_func(*, x):
            raise RuntimeError(f"fail with x={x}")

        mock = Mock(side_effect=faulty_func)

        @retry_deco(retries=1)
        def wrapped(*, x):
            return mock(x=x)

        with self.assertRaises(RuntimeError) as cm:
            wrapped(x=5)

        self.assertEqual(str(cm.exception), "fail with x=5")
        self.assertEqual(mock.call_count, 1)

    def test_multiple_expected_exceptions(self):
        mock = Mock(side_effect=[ValueError("bad value"), TypeError("wrong type")])

        @retry_deco(retries=2, expected_exceptions=[ValueError, TypeError])
        def wrapped():
            return mock()

        with self.assertRaises(TypeError) as cm:
            wrapped()

        self.assertEqual(str(cm.exception), "wrong type")
        self.assertEqual(mock.call_count, 2)
