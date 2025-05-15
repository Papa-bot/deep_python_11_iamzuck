import unittest
from unittest.mock import patch, MagicMock
import io
import json
import socket

import my_server
import client
# pylint: disable=too-few-public-methods
# pylint: disable=unused-argument


class FakeResponse:
    def __init__(self, data: bytes):
        self._data = data

    def read(self) -> bytes:
        return self._data

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class FakeConn:
    def __init__(self, recv_data: bytes):
        self._data = recv_data
        self.sent = b""
        self.closed = False

    def recv(self, bufsize: int) -> bytes:
        if self._data:
            d = self._data
            self._data = b""
            return d
        return b""

    def sendall(self, data: bytes) -> None:
        self.sent += data

    def close(self) -> None:
        self.closed = True


class TestServer(unittest.TestCase):
    def setUp(self):
        self.srv = my_server.Server("127.0.0.1", 0, workers=1, top_k=2)

    @patch("urllib.request.urlopen")
    def test_process_url_basic(self, mock_urlopen):
        mock_urlopen.return_value = FakeResponse(b"Hello world! Hello!!!")
        top = self.srv.process_url("http://ex")
        self.assertEqual(top, [("hello", 2), ("world", 1)])

    @patch("urllib.request.urlopen")
    def test_process_url_punctuation_and_case(self, mock_urlopen):
        mock_urlopen.return_value = FakeResponse(b"Abc, abc. AbC? xyz")
        top = self.srv.process_url("u")
        self.assertEqual(top, [("abc", 3), ("xyz", 1)])

    @patch("urllib.request.urlopen")
    def test_process_url_less_words_than_k(self, mock_urlopen):
        mock_urlopen.return_value = FakeResponse(b"one two one")
        self.srv.top_k = 5
        top = self.srv.process_url("u")
        self.assertEqual(len(top), 2)
        self.assertIn(("one", 2), top)
        self.assertIn(("two", 1), top)

    @patch.object(my_server.Server, "process_url", side_effect=ValueError("fail"))
    def test_worker_error_path(self, mock_proc):
        fake = FakeConn(b"http://test")
        calls = {"cnt": 0}

        def fake_get():
            if calls["cnt"] == 0:
                calls["cnt"] += 1
                return (fake, ("127.0.0.1", 1234))
            raise StopIteration()
        self.srv.queue = MagicMock(get=fake_get, task_done=lambda: None)
        with patch("builtins.print") as p:
            with self.assertRaises(StopIteration):
                self.srv.worker()
        self.assertTrue(fake.closed)
        p.assert_any_call("[error] fail")

    @patch.object(my_server.Server, "process_url", return_value=[("a", 1), ("b", 2)])
    def test_worker_send(self, mock_proc):
        fake = FakeConn(b"u")
        calls = {"cnt": 0}

        def fake_get():
            if calls["cnt"] == 0:
                calls["cnt"] += 1
                return (fake, ("127.0.0.1", 1))
            raise StopIteration()
        self.srv.queue = MagicMock(get=fake_get, task_done=lambda: None)
        self.srv.count = 0
        with patch("builtins.print"):
            with self.assertRaises(StopIteration):
                self.srv.worker()
        self.assertEqual(json.loads(fake.sent.decode()), {"a": 1, "b": 2})
        self.assertEqual(self.srv.count, 1)


class FakeSock:
    def __init__(self, response: bytes):
        self._response = response
        self._first = True

    def __enter__(self):
        return self

    def __exit__(self, *_):
        pass

    def sendall(self, data: bytes):
        pass

    def recv(self, bufsize: int) -> bytes:
        if self._first:
            self._first = False
            return self._response
        return b""


class TestClient(unittest.TestCase):
    def test_client_worker_success(self):
        urls = ["http://a"]
        cli = client.Client("h", "p", 1, urls)
        with patch("socket.create_connection", return_value=FakeSock(b'{"ok":1}')):
            buf = io.StringIO()
            with patch("sys.stdout", new=buf):
                cli.worker()
        out = buf.getvalue().strip()
        self.assertIn('http://a -> {"ok":1}', out)

    def test_client_worker_connection_error(self):
        urls = ["http://err"]
        cli = client.Client("h", "p", 1, urls)
        with patch("socket.create_connection", side_effect=socket.error("conn fail")):
            buf = io.StringIO()
            with patch("sys.stdout", new=buf):
                cli.worker()
        out = buf.getvalue()
        self.assertIn("[error] http://err: conn fail", out)

    def test_client_run_no_urls(self):
        cli = client.Client("h", "p", 1, [])
        cli.run()
