# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes
import socket
import threading
from collections import Counter
import re
import json
from urllib.request import urlopen
import argparse
from queue import Queue


class Worker(threading.Thread):
    def __init__(self, task_queue, k, lock, master):
        super().__init__()
        self.task_queue = task_queue
        self.k = k
        self.lock = lock
        self.master = master

    def fetch_url(self, url):
        try:
            with urlopen(url) as response:
                text = response.read().decode('utf-8')
            return text
        except Exception as e:  # pylint: disable=broad-except
            print(f"Ошибка при получении {url}: {e}")
            return ""

    def get_top_words(self, text):
        # Удаляем HTML-теги
        clean_text = re.sub(r'<[^>]+>', ' ', text)
        # Находим слова
        words = re.findall(r'\w+', clean_text.lower())
        word_counts = Counter(words)
        most_common = word_counts.most_common(self.k)
        return dict(most_common)

    def run(self):
        while True:
            url, client_socket = self.task_queue.get()
            if url is None:
                break
            text = self.fetch_url(url)
            result = self.get_top_words(text)
            client_socket.sendall(json.dumps(result).encode('utf-8'))
            client_socket.close()
            with self.lock:
                self.master.total_processed += 1
                print(f"Обработано URL адресов: {self.master.total_processed}")
            self.task_queue.task_done()


class MasterServer:
    def __init__(self, host, port, worker_count, k):
        self.host = host
        self.port = port
        self.worker_count = worker_count
        self.k = k
        self.task_queue = Queue()
        self.total_processed = 0
        self.lock = threading.Lock()
        self.workers = []

    def start(self):
        self.workers = [
            Worker(self.task_queue, self.k, self.lock, self)
            for _ in range(self.worker_count)
        ]
        for worker in self.workers:
            worker.start()

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen()

        print(f"Сервер запущен на: {self.host}:{self.port}")

        try:
            while True:
                client_socket, _ = server_socket.accept()
                url = client_socket.recv(4096).decode('utf-8')
                self.task_queue.put((url, client_socket))
        except KeyboardInterrupt:
            print("Выключение сервера...")
        finally:
            for _ in self.workers:
                self.task_queue.put((None, None))
            for worker in self.workers:
                worker.join()
            server_socket.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', default=1, type=int)
    parser.add_argument('-k', default=1, type=int)
    args = parser.parse_args()

    server = MasterServer('localhost', 8000, args.w, args.k)
    server.start()
