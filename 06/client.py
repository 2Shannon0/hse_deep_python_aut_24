import socket
import threading
import argparse


class ClientThread(threading.Thread):
    def __init__(self, url, server_host, server_port):
        super().__init__()
        self.url = url
        self.server_host = server_host
        self.server_port = server_port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.server_host, self.server_port))
            sock.sendall(self.url.encode('utf-8'))
            response = sock.recv(1024).decode('utf-8')
            print(f"{self.url}: {response}")


class Client:
    def __init__(self, url_file, thread_count, server_host, server_port):
        self.urls = self.load_urls(url_file)
        self.thread_count = thread_count
        self.server_host = server_host
        self.server_port = server_port

    def load_urls(self, url_file):
        with open(url_file, 'r', encoding='utf-8') as file:
            urls = [line.strip() for line in file]
        return urls

    def start(self):
        threads = []
        for url in self.urls:
            thread = ClientThread(url, self.server_host, self.server_port)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('thread_count')
    parser.add_argument('url_file')
    args = parser.parse_args()

    client = Client(args.url_file, args.thread_count, 'localhost', 8000)
    client.start()
