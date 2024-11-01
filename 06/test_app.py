import unittest
from unittest.mock import patch, Mock, MagicMock
from server import Worker
from client import Client, ClientThread


class TestWorker(unittest.TestCase):

    def test_get_top_words(self):
        task_queue = Mock()
        lock = Mock()
        master = Mock()
        worker = Worker(task_queue, 3, lock, master)

        text = "<html><body>Hello World Hello</body></html>"
        result = worker.get_top_words(text)

        expected = {"hello": 2, "world": 1}
        self.assertEqual(result, expected)

    def test_get_top_words_empty(self):
        task_queue = Mock()
        lock = Mock()
        master = Mock()
        worker = Worker(task_queue, 3, lock, master)

        text = "<html><body></body></html>"
        result = worker.get_top_words(text)

        expected = {}
        self.assertEqual(result, expected)


class TestClient(unittest.TestCase):
    @patch('builtins.open',
           new_callable=unittest.mock.mock_open,
           read_data='http://example.com\nhttp://example.org\n')
    def test_load_urls(self):
        client = Client('fake_file.txt', 2, 'localhost', 8000)
        expected_urls = ['http://example.com', 'http://example.org']
        self.assertEqual(client.urls, expected_urls)

    @patch('socket.socket')
    def test_client_thread_run(self, mock_socket):
        mock_sock_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_sock_instance
        url = 'http://example.com'
        thread = ClientThread(url, 'localhost', 8000)
        thread.start()
        thread.join()

        mock_sock_instance.connect.assert_called_once_with(('localhost', 8000))
        mock_sock_instance.sendall.assert_called_once_with(url.encode('utf-8'))

    @patch('socket.socket')
    def test_client_start(self, mock_socket):
        mock_sock_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_sock_instance

        with patch('builtins.open',
                   new_callable=unittest.mock.mock_open,
                   read_data='http://example.com\n'):
            client = Client('fake_file.txt', 2, 'localhost', 8000)
            client.start()

            mock_sock_instance.connect.assert_called_once_with(
                    ('localhost', 8000)
                )
            mock_sock_instance.sendall.assert_called_once_with(
                    'http://example.com'.encode('utf-8')
                )
