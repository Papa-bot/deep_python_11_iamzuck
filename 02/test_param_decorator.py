import unittest
from unittest.mock import Mock, call, patch
from param_decorator import retry_deco


class TestRetryDeco(unittest.TestCase):

    def test_success_first_try(self):
        mock = Mock(return_value=42)

        @retry_deco(retries=3)
        def wrapped():
            return mock()

        with patch("builtins.print") as mock_print:
            result = wrapped()
        self.assertEqual(result, 42)
        self.assertEqual(mock.call_count, 1)

        expected_calls = [
            call('\nrun "wrapped" attempt = 1 result = 42')
        ]
        mock_print.assert_has_calls(expected_calls)

    def test_retry_until_success(self):
        mock = Mock(side_effect=[Exception("fail"), Exception("fail again"), 100])

        @retry_deco(retries=3)
        def wrapped():
            return mock()

        with patch("builtins.print") as mock_print:
            result = wrapped()
        self.assertEqual(result, 100)
        self.assertEqual(mock.call_count, 3)

        expected_calls = [
            call('\nrun "wrapped" attempt = 1 exception = Exception'),
            call('\nrun "wrapped" attempt = 2 exception = Exception'),
            call('\nrun "wrapped" attempt = 3 result = 100')
        ]
        mock_print.assert_has_calls(expected_calls)

    def test_stop_on_expected_exception_and_raise_it(self):
        mock = Mock(side_effect=ValueError("bad value"))

        @retry_deco(retries=5, expected_exceptions=[ValueError])
        def wrapped():
            return mock()

        with patch("builtins.print") as mock_print:
            with self.assertRaises(ValueError) as cm:
                wrapped()

        self.assertEqual(str(cm.exception), "bad value")
        self.assertEqual(mock.call_count, 1)

        expected_calls = [
            call('\nrun "wrapped" attempt = 1 exception = ValueError')
        ]
        mock_print.assert_has_calls(expected_calls)

    def test_continue_on_unexpected_exception_and_raise_last_one(self):
        mock = Mock(side_effect=[KeyError("unexpected"), KeyError("again"), TypeError("final")])

        @retry_deco(retries=3, expected_exceptions=[ValueError])
        def wrapped():
            return mock()

        with patch("builtins.print") as mock_print:
            with self.assertRaises(TypeError) as cm:
                wrapped()

        self.assertEqual(str(cm.exception), "final")
        self.assertEqual(mock.call_count, 3)

        expected_calls = [
            call('\nrun "wrapped" attempt = 1 exception = KeyError'),
            call('\nrun "wrapped" attempt = 2 exception = KeyError'),
            call('\nrun "wrapped" attempt = 3 exception = TypeError')
        ]
        mock_print.assert_has_calls(expected_calls)

    def test_args_and_kwargs_combination(self):
        mock = Mock(side_effect=lambda x, y=0: x + y)

        @retry_deco(retries=2)
        def wrapped(x, y=0):
            return mock(x, y=y)

        with patch("builtins.print") as mock_print:
            result = wrapped(1, y=2)

        self.assertEqual(result, 3)
        self.assertEqual(mock.call_args, call(1, y=2))

        expected_calls = [
            call('\nrun "wrapped" with positional args = (1,) keyword kwargs = {\'y\': 2} attempt = 1 result = 3')
        ]
        mock_print.assert_has_calls(expected_calls)

    def test_retries_equals_one_with_exception(self):
        mock = Mock(side_effect=Exception("fail"))

        @retry_deco(retries=1)
        def wrapped():
            return mock()

        with patch("builtins.print") as mock_print:
            with self.assertRaises(Exception) as cm:
                wrapped()

        self.assertEqual(str(cm.exception), "fail")
        self.assertEqual(mock.call_count, 1)

        expected_calls = [
            call('\nrun "wrapped" attempt = 1 exception = Exception')
        ]
        mock_print.assert_has_calls(expected_calls)

    def test_expected_exception_is_none(self):
        mock = Mock(side_effect=[TypeError("fail"), 100])

        @retry_deco(retries=2, expected_exceptions=None)
        def wrapped():
            return mock()

        with patch("builtins.print") as mock_print:
            result = wrapped()
        self.assertEqual(result, 100)
        self.assertEqual(mock.call_count, 2)

        expected_calls = [
            call('\nrun "wrapped" attempt = 1 exception = TypeError'),
            call('\nrun "wrapped" attempt = 2 result = 100')
        ]
        mock_print.assert_has_calls(expected_calls)

    def test_only_kwargs(self):
        mock = Mock(side_effect=lambda *, x: x * 2)

        @retry_deco(retries=2)
        def wrapped(*, x):
            return mock(x=x)

        with patch("builtins.print") as mock_print:
            result = wrapped(x=5)

        self.assertEqual(result, 10)
        self.assertEqual(mock.call_count, 1)

        expected_calls = [
            call('\nrun "wrapped" with keyword kwargs = {\'x\': 5} attempt = 1 result = 10')
        ]
        mock_print.assert_has_calls(expected_calls)

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

    def test_zero_retries_raises_immediately(self):
        mock = Mock(side_effect=Exception("should not be called"))

        @retry_deco(retries=0)
        def wrapped():
            return mock()

        with patch("builtins.print") as mock_print:
            with self.assertRaises(Exception) as cm:
                wrapped()

        self.assertEqual(str(cm.exception), "Function not attempted (retries=0)")
        self.assertEqual(mock.call_count, 0)

        expected_calls = []
        mock_print.assert_has_calls(expected_calls)

    def test_negative_retries_raises_immediately(self):
        with patch("builtins.print") as mock_print:
            with self.assertRaises(ValueError) as cm:
                @retry_deco(retries=-5)
                def wrapped():
                    pass
        self.assertEqual(str(cm.exception), "retries cannot be negative")

        expected_calls = []
        mock_print.assert_has_calls(expected_calls)

    def test_invalid_retries_type(self):
        with self.assertRaisesRegex(TypeError, "retries must be an integer"):
            @retry_deco(retries="three")
            def wrapped():
                return 1
            wrapped()

    def test_all_attempts_fail_raise_last_exception(self):
        mock = Mock(side_effect=[Exception("fail1"), Exception("fail2"), Exception("fail3")])

        @retry_deco(retries=3)
        def wrapped():
            return mock()

        with patch("builtins.print") as mock_print:
            with self.assertRaises(Exception) as cm:
                wrapped()

        self.assertEqual(str(cm.exception), "fail3")
        self.assertEqual(mock.call_count, 3)

        expected_calls = [
            call('\nrun "wrapped" attempt = 1 exception = Exception'),
            call('\nrun "wrapped" attempt = 2 exception = Exception'),
            call('\nrun "wrapped" attempt = 3 exception = Exception')
        ]
        mock_print.assert_has_calls(expected_calls)

    def test_exception_with_args_and_kwargs_raised_properly(self):
        def faulty_func(x, y=0):
            raise RuntimeError(f"fail with x={x} y={y}")

        mock = Mock(side_effect=faulty_func)

        @retry_deco(retries=1)
        def wrapped(x, y=0):
            return mock(x, y=y)

        with patch("builtins.print") as mock_print:
            with self.assertRaises(RuntimeError) as cm:
                wrapped(1, y=2)

        self.assertEqual(str(cm.exception), "fail with x=1 y=2")
        self.assertEqual(mock.call_count, 1)

        expected_calls = [
            call('\nrun "wrapped" '
                 'with positional args = (1,) '
                 'keyword kwargs = {\'y\': 2} '
                 'attempt = 1 '
                 'exception = RuntimeError')
        ]
        mock_print.assert_has_calls(expected_calls)

    def test_exception_with_only_kwargs_raised_properly(self):
        def faulty_func(*, x):
            raise RuntimeError(f"fail with x={x}")

        mock = Mock(side_effect=faulty_func)

        @retry_deco(retries=1)
        def wrapped(*, x):
            return mock(x=x)

        with patch("builtins.print") as mock_print:
            with self.assertRaises(RuntimeError) as cm:
                wrapped(x=5)

        self.assertEqual(str(cm.exception), "fail with x=5")
        self.assertEqual(mock.call_count, 1)

        expected_calls = [
            call('\nrun "wrapped" with keyword kwargs = {\'x\': 5} attempt = 1 exception = RuntimeError')
        ]
        mock_print.assert_has_calls(expected_calls)

    def test_multiple_expected_exceptions(self):
        mock = Mock(side_effect=[ValueError("bad value"), TypeError("wrong type")])

        @retry_deco(retries=2, expected_exceptions=[ValueError, TypeError])
        def wrapped():
            return mock()

        with patch("builtins.print") as mock_print:
            with self.assertRaises(ValueError) as cm:
                wrapped()

        self.assertEqual(str(cm.exception), "bad value")
        self.assertEqual(mock.call_count, 1)

        expected_calls = [
            call('\nrun "wrapped" attempt = 1 exception = ValueError')
        ]
        mock_print.assert_has_calls(expected_calls)
