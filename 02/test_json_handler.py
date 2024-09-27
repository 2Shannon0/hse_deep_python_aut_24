import unittest
from unittest.mock import patch
from io import StringIO


from json_handler import process_json


class TestJsonHandler(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test0_find_tokens_from_example(self, mock_stdout):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "KEY2"]
        tokens = ["WORD1", "word2"]
        process_json(
            json_str,
            required_keys,
            tokens,
            lambda key, token: print(f"{key=}, {token=}")
        )
        expected_output = (
            "key='key1', token='WORD1'\n"
            "key='key1', token='word2'\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test1_find_tokens_change_registr_in_key(self, mock_stdout):
        json_str = '{"kEy1": "Word1 word2", "key2": "wOrd2 word3"}'
        required_keys = ["key1", "KEY2"]
        tokens = ["WORD1", "word2"]
        process_json(
            json_str,
            required_keys,
            tokens,
            lambda key, token: print(f"{key=}, {token=}")
        )
        expected_output = (
            ''  # вывод отсутствует
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test2_find_tokens(self, mock_stdout):
        json_str = '{"key1": "Word1 word2", "key2": "wOrd2 word3"}'
        required_keys = ["key1", "key2"]
        tokens = ["WORD1", "word2"]
        process_json(
            json_str,
            required_keys,
            tokens,
            lambda key, token: print(f"{key=}, {token=}")
        )
        expected_output = (
            "key='key1', token='WORD1'\n"
            "key='key1', token='word2'\n"
            "key='key2', token='word2'\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test3_run_without_required_keys(self, mock_stdout):
        json_str = '{"key1": "Word1 word2", "key2": "wOrd2 word3"}'
        required_keys = []
        tokens = ["WORD1", "word2"]
        process_json(
            json_str,
            required_keys,
            tokens,
            lambda key, token: print(f"{key=}, {token=}")
        )
        expected_output = 'required_keys list is empty\n'
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test4_run_without_tokens(self, mock_stdout):
        json_str = '{"key1": "Word1 word2", "key2": "wOrd2 word3"}'
        required_keys = ["key1", "key2"]
        tokens = []
        process_json(
            json_str,
            required_keys,
            tokens,
            lambda key, token: print(f"{key=}, {token=}")
        )
        expected_output = 'tokens list is empty\n'
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test5_run_without_collback(self, mock_stdout):
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "KEY2"]
        tokens = ["WORD1", "word2"]
        process_json(
            json_str,
            required_keys,
            tokens,
        )
        expected_output = (
            ''  # вывод отсутствует
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test6_run_json_str_is_empty(self, mock_stdout):
        json_str = ''
        required_keys = ["key1", "KEY2"]
        tokens = ["WORD1", "word2"]
        process_json(
            json_str,
            required_keys,
            tokens,
        )
        expected_output = (
            ''  # вывод отсутствует
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test7_find_tokens_many(self, mock_stdout):
        json_str = '''
            {
                "key1": "Word1 word2",
                "key2": "wOrd2 word3",
                "key3": "wOrd2 word1 word5",
                "key4": "wOrd2 word3",
                "key5": "wOrd1 word3 Word555",
                "Key6": "wOrd2 word3"

            }
        '''
        required_keys = ["key1", "KEY2", "key3", "key5", "key6"]
        tokens = ["WORD1", "word2", "word555"]
        process_json(
            json_str,
            required_keys,
            tokens,
            lambda key, token: print(f"{key=}, {token=}")
        )
        expected_output = (
            "key='key1', token='WORD1'\n"
            "key='key1', token='word2'\n"
            "key='key3', token='WORD1'\n"
            "key='key3', token='word2'\n"
            "key='key5', token='WORD1'\n"
            "key='key5', token='word555'\n"


        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)
