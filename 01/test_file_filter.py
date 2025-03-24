import unittest
from io import StringIO
import tempfile
import os

from file_filter import filter_lines


class TestFilterLines(unittest.TestCase):
    def setUp(self):
        self.data = '''роза упала на лапу Азора

                       ветер гонит листья по дороге
                       луна светит над лесом
                       роза цветет в саду
                       день прекрасен когда нет дождя'''
        self.file_obj = StringIO(self.data)

    def test_basic_match(self):
        search = ['роза', 'луна']
        stop = []
        expected = ['роза упала на лапу Азора',
                    'луна светит над лесом',
                    'роза цветет в саду']
        result = list(filter_lines(self.file_obj, search, stop))
        self.assertEqual(expected, result)

    def test_stop_word_exclusion(self):
        search = ['роза']
        stop = ['азора']
        expected = ['роза цветет в саду']
        self.file_obj.seek(0)
        result = list(filter_lines(self.file_obj, search, stop))
        self.assertEqual(expected, result)

    def test_no_matches(self):
        search = ['test']
        stop = []
        expected = []
        self.file_obj.seek(0)
        result = list(filter_lines(self.file_obj, search, stop))
        self.assertEqual(expected, result)

    def test_stop_word_only(self):
        search = ['луна']
        stop = ['луна']
        expected = []
        self.file_obj.seek(0)
        result = list(filter_lines(self.file_obj, search, stop))
        self.assertEqual(expected, result)

    def test_case_insensitivity(self):
        search = ['рОза']
        stop = ['аЗорА']
        expected = ['роза цветет в саду']
        self.file_obj.seek(0)
        result = list(filter_lines(self.file_obj, search, stop))
        self.assertEqual(expected, result)

    def test_with_file_path(self):
        search = ['роза']
        stop = []
        expected = ['роза упала на лапу Азора', 'роза цветет в саду']

        with tempfile.NamedTemporaryFile(
            delete=False, mode='w', encoding='utf-8'
        ) as tmp:
            tmp.write(self.data)
            tmp_path = tmp.name

        try:
            result = list(filter_lines(tmp_path, search, stop))
            self.assertEqual(result, expected)
        finally:
            os.remove(tmp_path)
