import argparse
import socket
import threading
import urllib.request
import re
import json
from collections import Counter
from queue import Queue
from typing import Tuple, List
# pylint: disable=broad-exception-caught
# pylint: disable=unused-variable


class Server:
    def __init__(self, host: str, port: int, workers: int, top_k: int):
        self.host = host
        self.port = port
        self.workers = workers
        self.top_k = top_k
        self.queue: Queue[Tuple[socket.socket, Tuple[str, int]]] = Queue()
        self.count = 0
        self.lock = threading.Lock()

    def process_url(self, url: str) -> List[Tuple[str, int]]:
        with urllib.request.urlopen(url, timeout=10) as resp:
            text = resp.read().decode(errors='ignore').lower()
        words = re.findall(r'\w+', text)
        return Counter(words).most_common(self.top_k)

    def worker(self) -> None:
        while True:
            conn, addr = self.queue.get()
            try:
                data = conn.recv(4096).decode().strip()
                top = self.process_url(data)
                conn.sendall(json.dumps(dict(top)).encode())
                with self.lock:
                    self.count += 1
                    print(f"[stat] processed = {self.count}")
            except Exception as e:
                print(f"[error] {e}")
            finally:
                conn.close()
                self.queue.task_done()

    def serve(self) -> None:
        for _ in range(self.workers):
            t = threading.Thread(target=self.worker, daemon=True)
            t.start()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen()
            print(f"[info] Listening on {self.host}:{self.port}")
            while True:
                conn, addr = s.accept()
                self.queue.put((conn, addr))


def main():
    parser = argparse.ArgumentParser(description="Master-worker HTTP-scraper server")
    parser.add_argument("-w", "--workers", type=int, required=True, help="Number of worker threads")
    parser.add_argument("-k", "--topk", type=int,    required=True, help="Top K frequent words to return")
    parser.add_argument("-H", "--host", default="0.0.0.0", help="Bind host (default: 0.0.0.0)")
    parser.add_argument("-P", "--port", type=int, default=8000, help="Bind port (default: 8000)")
    args = parser.parse_args()

    srv = Server(args.host, args.port, args.workers, args.topk)
    srv.serve()


if __name__ == "__main__":
    main()
