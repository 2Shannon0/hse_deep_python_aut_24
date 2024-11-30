import unittest
from unittest.mock import patch
from io import StringIO

from cust_decorator import add, check_str, check_int


class TestDecarator(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test1_add(self, mock_stdout):

        add(2, 5)

        expected_output = (
            'run "add" with positional args = (2, 5), attempt = 1, result = 7\n'
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test2_add(self, mock_stdout):

        add(2, b=5)

        expected_output = (
             'run "add" with positional args = (2,), '
             'keyword kwargs = {\'b\': 5}, '
             'attempt = 1, result = 7\n'
            )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test5_check_str(self, mock_stdout):

        check_str('hse')

        expected_output = (
             'run "check_str" with positional args = (\'hse\',), '
             'attempt = 1, result = True\n'
            )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    # "тесты декоратора по кейсам из задания и с выбросами ошибок:"

    @patch('sys.stdout', new_callable=StringIO)
    def test_add_4_2(self, mock_stdout):

        add(4, 2)

        expected_output = (
            'run "add" with positional args = (4, 2), attempt = 1, result = 6\n'
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_add_4_3(self, mock_stdout):

        add(4, b=3)

        expected_output = (
            'run "add" with positional args = (4,), '
            'keyword kwargs = {\'b\': 3},'
            ' attempt = 1, result = 7\n'
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_check_str_123(self, mock_stdout):

        check_str(value="123")

        expected_output = (
            'run "check_str" with keyword kwargs = {\'value\': \'123\'}, '
            'attempt = 1, result = True\n'
            )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_check_str_1(self, mock_stdout):

        check_str(value=1)

        expected_output = (
            'run "check_str" with keyword kwargs = {\'value\': 1}, '
            'attempt = 1, result = False\n'
            )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_check_str_none(self, mock_stdout):

        with self.assertRaises(ValueError):
            check_str(value=None)

        expected_output = (
             'run "check_str" with keyword kwargs = {\'value\': None}, '
             'attempt = 1, exception = ValueError\n'
             'run "check_str" with keyword kwargs = {\'value\': None}, '
             'attempt = 2, exception = ValueError\n'
             'run "check_str" with keyword kwargs = {\'value\': None}, '
             'attempt = 3, exception = ValueError\n'
            )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_check_int_1(self, mock_stdout):

        check_int(value=1)

        expected_output = (
            'run "check_int" with keyword kwargs = {\'value\': 1}, '
            'attempt = 1, result = True\n'
            )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_check_int_none(self, mock_stdout):

        with self.assertRaises(ValueError):
            check_int(value=None)

        expected_output = (
            'run "check_int" with keyword kwargs = {\'value\': None}, '
            'attempt = 1, exception = ValueError\n'
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)
