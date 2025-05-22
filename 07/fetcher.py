import argparse
import asyncio
import dataclasses as dc
import sys
from pathlib import Path
import aiohttp
# pylint: disable=too-few-public-methods
# pylint: disable=broad-exception-caught


@dc.dataclass(slots=True)
class Res:
    url: str
    status: int
    size: int


async def _get(s, u: str, sem: asyncio.Semaphore) -> Res:
    async with sem:
        try:
            async with s.get(u) as r:
                d = await r.read()
                return Res(u, r.status, len(d))
        except Exception:
            return Res(u, -1, 0)


async def fetch_all(urls: list[str], c: int) -> list[Res]:
    sem = asyncio.Semaphore(c)
    async with aiohttp.ClientSession() as s:
        t = [asyncio.create_task(_get(s, u, sem)) for u in urls]
        return await asyncio.gather(*t)


def _cli() -> tuple[int, Path]:
    p = argparse.ArgumentParser()
    p.add_argument("file", type=Path, help="Файл со списком URL-ов")
    p.add_argument("-c", "--concurrency", type=int, default=10, help="Параллельных запросов")
    a = p.parse_args()
    return a.concurrency, a.file


def main() -> None:
    c, f = _cli()
    if not f.exists():
        sys.exit(f"no file {f}")
    urls = [u.strip() for u in f.read_text().splitlines() if u.strip()]
    res = asyncio.run(fetch_all(urls, c))
    ok = [r for r in res if r.status == 200]
    err = [r for r in res if r.status != 200]
    print(f"ok: {len(ok)}  err: {len(err)}  bytes: {sum(r.size for r in ok)}")


if __name__ == "__main__":
    main()
