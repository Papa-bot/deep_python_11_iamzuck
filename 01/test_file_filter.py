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

    def test_match_multiple_filters_in_one_line(self):
        search = ['ветер', 'гонит', 'луна', 'светит']
        stop = ['луна', 'светит']
        expected = ['ветер гонит листья по дороге']
        self.file_obj.seek(0)
        result = list(filter_lines(self.file_obj, search, stop))
        self.assertEqual(expected, result)

    def test_match_with_whole_line(self):
        search = ['ветер гонит листья по дороге']
        stop = ['луна светит над лесом']
        expected = []
        self.file_obj.seek(0)
        result = list(filter_lines(self.file_obj, search, stop))
        self.assertEqual(expected, result)

    def test_exact_word_match(self):
        data = 'роза\nлуна\nроза\nдорога\n'
        search = ['роза']
        stop = []
        expected = ['роза', 'роза']
        result = list(filter_lines(StringIO(data), search, stop))
        self.assertEqual(expected, result)

    def test_empty_filter(self):
        search = ['']
        stop = ['']
        expected = []
        self.file_obj.seek(0)
        result = list(filter_lines(self.file_obj, search, stop))
        self.assertEqual(expected, result)

    def test_one_letter(self):
        search = ['в']
        stop = ['р']
        expected = ['роза цветет в саду']
        self.file_obj.seek(0)
        result = list(filter_lines(self.file_obj, search, stop))
        self.assertEqual(expected, result)

    def test_numeric_and_mixed_words(self):
        data = 'строка с цифрами 123\nстрока смешанная A1Б2В3\n'
        search = ['A1Б2В3']
        stop = ['123']
        expected = ['строка смешанная A1Б2В3']
        result = list(filter_lines(StringIO(data), search, stop))
        self.assertEqual(expected, result)

    def test_repeated(self):
        data = 'роза\nроза\nроза\n'
        search = ['роза']
        stop = []
        expected = ['роза', 'роза', 'роза']
        result = list(filter_lines(StringIO(data), search, stop))
        self.assertEqual(expected, result)
