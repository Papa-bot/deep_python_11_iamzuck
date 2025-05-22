import asyncio
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import fetcher
from fetcher import Res
# pylint: disable=protected-access


class TestGet(unittest.IsolatedAsyncioTestCase):
    async def test__get_success(self):
        url = "http://example.com"
        data = b"hello"
        mock_resp = mock.AsyncMock()
        mock_resp.status = 200
        mock_resp.read.return_value = data
        mock_ctx = mock.AsyncMock()
        mock_ctx.__aenter__.return_value = mock_resp
        mock_sess = mock.MagicMock()
        mock_sess.get.return_value = mock_ctx

        sem = asyncio.Semaphore(1)
        res = await fetcher._get(mock_sess, url, sem)
        self.assertEqual(res.url, url)
        self.assertEqual(res.status, 200)
        self.assertEqual(res.size, len(data))

    async def test__get_error_status(self):
        url = "http://example.com/notfound"
        data = b""
        mock_resp = mock.AsyncMock()
        mock_resp.status = 404
        mock_resp.read.return_value = data
        mock_ctx = mock.AsyncMock()
        mock_ctx.__aenter__.return_value = mock_resp
        mock_sess = mock.MagicMock()
        mock_sess.get.return_value = mock_ctx

        sem = asyncio.Semaphore(1)
        res = await fetcher._get(mock_sess, url, sem)
        self.assertEqual(res.status, 404)
        self.assertEqual(res.size, 0)

    async def test__get_exception(self):
        url = "http://bad.url"

        def raise_exc(u):
            raise RuntimeError("fail")
        mock_sess = mock.MagicMock()
        mock_sess.get.side_effect = raise_exc

        sem = asyncio.Semaphore(1)
        res = await fetcher._get(mock_sess, url, sem)
        self.assertEqual(res.status, -1)
        self.assertEqual(res.size, 0)


class TestFetchAll(unittest.IsolatedAsyncioTestCase):
    async def test_fetch_all_uses_get(self):
        urls = ["u1", "u2"]
        fake = [
            Res("u1", 200, 10),
            Res("u2", 500, 0),
        ]
        with mock.patch.object(fetcher, "_get", new_callable=mock.AsyncMock) as mget:
            mget.side_effect = fake
            result = await fetcher.fetch_all(urls, c=2)
            self.assertEqual(result, fake)
            mget.assert_any_await(mock.ANY, "u1", mock.ANY)
            mget.assert_any_await(mock.ANY, "u2", mock.ANY)


class TestCLI(unittest.TestCase):
    def test__cli_defaults(self):
        argv = ["prog", "file.txt"]
        with mock.patch.object(sys, "argv", argv):
            c, f = fetcher._cli()
            self.assertEqual(c, 10)
            self.assertEqual(f, Path("file.txt"))

    def test__cli_custom(self):
        argv = ["prog", "my.txt", "-c", "5"]
        with mock.patch.object(sys, "argv", argv):
            c, f = fetcher._cli()
            self.assertEqual(c, 5)
            self.assertEqual(f, Path("my.txt"))


class TestMain(unittest.TestCase):
    def test_main_no_file(self):
        argv = ["prog", "nofile.txt"]
        with mock.patch.object(sys, "argv", argv):
            if Path("nofile.txt").exists():
                Path("nofile.txt").unlink()
            with self.assertRaises(SystemExit) as cm:
                fetcher.main()
            self.assertIn("no file nofile.txt", str(cm.exception))

    def test_main_success(self):
        with tempfile.NamedTemporaryFile("w+", delete=False) as t:
            t.write("http://ok\nhttp://err\n")
            t.flush()
            tmp_path = Path(t.name)

        argv = ["prog", str(tmp_path), "-c", "3"]
        fake_res = [
            Res("u1", 200, 5),
            Res("u2", 500, 0),
        ]
        with mock.patch.object(sys, "argv", argv), \
             mock.patch.object(fetcher, "fetch_all", new_callable=mock.AsyncMock) as mfetch, \
             mock.patch("builtins.print") as mprint:
            mfetch.return_value = fake_res
            fetcher.main()
            mprint.assert_called_once_with("ok: 1  err: 1  bytes: 5")

        tmp_path.unlink()
