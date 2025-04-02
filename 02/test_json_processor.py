import unittest
import json
from unittest.mock import Mock
from json_handler import process_json


class TestProcessJson(unittest.TestCase):
    def setUp(self):
        self.sample_json = '{"key1": "value1 value2", "key2": "value2 value3"}'
        self.sample_tokens = ["value1", "VALUE2"]
        self.required_keys = ["key1", "key2"]
        self.mock_callback = Mock()

    def test_normal_case(self):
        process_json(self.sample_json, self.required_keys, self.sample_tokens, self.mock_callback)
        expected_calls = [
            (('key1', 'value1'),),
            (('key1', 'value2'),),
            (('key2', 'value2'),),
        ]
        self.assertEqual(self.mock_callback.call_args_list, expected_calls)

    def test_no_required_keys(self):
        process_json(self.sample_json, None, self.sample_tokens, self.mock_callback)
        self.mock_callback.assert_not_called()

    def test_no_tokens(self):
        process_json(self.sample_json, self.required_keys, None, self.mock_callback)
        self.mock_callback.assert_not_called()

    def test_no_callback(self):
        process_json(self.sample_json, self.required_keys, self.sample_tokens, None)
        self.mock_callback.assert_not_called()

    def test_case_insensitive_matching(self):
        json_str = '{"key1": "VALUE1 Value2"}'
        process_json(json_str, ["key1"], ["vAlUe1", "value2"], self.mock_callback)
        expected_calls = [
            (('key1', 'VALUE1'),),
            (('key1', 'Value2'),),
        ]
        self.assertEqual(self.mock_callback.call_args_list, expected_calls)

    def test_no_matches(self):
        json_str = '{"key1": "some other value"}'
        process_json(json_str, ["key1"], ["non_matching"], self.mock_callback)
        self.mock_callback.assert_not_called()

    def test_empty_json(self):
        process_json("{}", self.required_keys, self.sample_tokens, self.mock_callback)
        self.mock_callback.assert_not_called()

    def test_invalid_json(self):
        with self.assertRaises(json.JSONDecodeError):
            process_json("{invalid}", self.required_keys, self.sample_tokens, self.mock_callback)

    def test_invalid_json_str_type(self):
        with self.assertRaises(TypeError):
            process_json(123, self.required_keys, self.sample_tokens, self.mock_callback)

    def test_invalid_required_keys_type(self):
        with self.assertRaises(TypeError):
            process_json(self.sample_json, ["key1", 123], self.sample_tokens, self.mock_callback)

    def test_invalid_tokens_type(self):
        with self.assertRaises(TypeError):
            process_json(self.sample_json, self.required_keys, ["token1", 456], self.mock_callback)

    def test_invalid_callback_type(self):
        with self.assertRaises(TypeError):
            process_json(self.sample_json, self.required_keys, self.sample_tokens, "not a callable")

    def test_partial_required_keys(self):
        json_str = '{"key1": "match", "key2": "no match", "key3": "match"}'
        process_json(json_str, ["key1", "key3"], ["match"], self.mock_callback)

        expected_calls = [
            (('key1', 'match'),),
            (('key3', 'match'),),
        ]
        self.assertEqual(self.mock_callback.call_args_list, expected_calls)

    def test_multiple_matches_in_single_value(self):
        json_str = '{"key1": "word word word"}'
        process_json(json_str, ["key1"], ["word"], self.mock_callback)

        expected_calls = [
            (('key1', 'word'),),
            (('key1', 'word'),),
            (('key1', 'word'),),
        ]
        self.assertEqual(self.mock_callback.call_args_list, expected_calls)

    def test_empty_tokens(self):
        process_json(self.sample_json, self.required_keys, [], self.mock_callback)
        self.mock_callback.assert_not_called()

    def test_empty_required_keys(self):
        process_json(self.sample_json, [], self.sample_tokens, self.mock_callback)
        self.mock_callback.assert_not_called()
