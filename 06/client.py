import argparse
import socket
import threading
from queue import Queue
from typing import List
# pylint: disable=broad-exception-caught


class Client:
    def __init__(self, host: str, port: int, n_threads: int, urls: List[str]):
        self.host = host
        self.port = port
        self.n_threads = n_threads
        self.queue: Queue[str] = Queue()
        for url in urls:
            self.queue.put(url)

    def worker(self) -> None:
        while True:
            try:
                url = self.queue.get_nowait()
            except Exception:
                break
            try:
                with socket.create_connection((self.host, self.port), timeout=5) as s:
                    s.sendall(url.encode())
                    data = b""
                    while chunk := s.recv(4096):
                        data += chunk
                print(f"{url} -> {data.decode()}")
            except Exception as e:
                print(f"[error] {url}: {e}")
            finally:
                self.queue.task_done()

    def run(self) -> None:
        threads = []
        for _ in range(self.n_threads):
            t = threading.Thread(target=self.worker)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()


def main():
    parser = argparse.ArgumentParser(description="Multi-threaded TCP client for URL scraping")
    parser.add_argument("threads", type=int, help="Number of concurrent threads")
    parser.add_argument("file",    help="Path to file with URLs (one per line)")
    parser.add_argument("-H", "--host", default="127.0.0.1", help="Server host (default: 127.0.0.1)")
    parser.add_argument("-P", "--port", type=int, default=8000, help="Server port (default: 8000)")
    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    cli = Client(args.host, args.port, args.threads, urls)
    cli.run()


if __name__ == "__main__":
    main()
