from __future__ import annotations

import argparse
import logging
import sys
from collections import OrderedDict
from typing import Any, Final, Optional

_LOGGER_NAME: Final[str] = "lru_cache"
LOG = logging.getLogger(_LOGGER_NAME)
# pylint: disable=too-few-public-methods
# pylint: disable=redefined-outer-name


class OddWordsFilter(logging.Filter):

    def filter(self, record: logging.LogRecord) -> bool:
        words = record.getMessage().split()
        return len(words) % 2 == 1


def configure_logging(to_stdout: bool = False, use_filter: bool = False) -> None:
    root = logging.getLogger()
    if root.handlers:
        return

    root.setLevel(logging.DEBUG)

    fh = logging.FileHandler("cache.log", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    root.addHandler(fh)

    if to_stdout:
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.INFO)
        sh.setFormatter(logging.Formatter("▶ %(levelname)s: %(message)s"))
        root.addHandler(sh)

    if use_filter:
        odd_filter = OddWordsFilter()
        for handler in root.handlers:
            handler.addFilter(odd_filter)


class LRUCache:

    def __init__(self, capacity: int = 128) -> None:
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self._capacity: int = capacity
        self._data: OrderedDict[Any, Any] = OrderedDict()
        LOG.debug("Initialized cache with capacity %d", capacity)

    def get(self, key: Any) -> Optional[Any]:
        if key in self._data:
            value = self._data.pop(key)
            self._data[key] = value
            LOG.info("Get existing key '%s' → %s", key, value)
            return value
        LOG.warning("Get *missing* key '%s'", key)
        return None

    def set(self, key: Any, value: Any) -> None:
        if key in self._data:
            self._data.pop(key)
            self._data[key] = value
            LOG.info("Set *existing* key '%s' → %s", key, value)
            return

        if len(self._data) >= self._capacity:
            evicted_key, evicted_val = self._data.popitem(last=False)
            LOG.info(
                "Capacity reached – evicting LRU key '%s' (value %s)",
                evicted_key,
                evicted_val,
            )
        self._data[key] = value
        LOG.info("Set *new* key '%s' → %s", key, value)

    def __contains__(self, key: Any) -> bool:
        return key in self._data

    def __len__(self) -> int:
        return len(self._data)


def _demo() -> None:
    cache = LRUCache(capacity=2)

    cache.set("a", 1)
    cache.set("b", 2)

    _ = cache.get("a")

    _ = cache.get("z")

    cache.set("c", 3)

    cache.set("a", 42)

    LOG.debug("Done exercising the cache – current size is %d", len(cache))


def _parse_cli() -> tuple[bool, bool]:
    parser = argparse.ArgumentParser(description="LRU-Cache logging demo")
    parser.add_argument(
        "-s",
        "--stdout",
        action="store_true",
        help="Duplicate log output to stdout with a friendly formatter.",
    )
    parser.add_argument(
        "-f",
        "--filter",
        action="store_true",
        help="Apply the OddWordsFilter (drops even-worded messages).",
    )
    ns = parser.parse_args()
    return ns.stdout, ns.filter


if __name__ == "__main__":
    to_stdout, use_filter = _parse_cli()
    configure_logging(to_stdout=to_stdout, use_filter=use_filter)

    LOG.info("⇢ Starting demonstration – filter=%s stdout=%s", use_filter, to_stdout)
    _demo()
    LOG.info("⇠ Demo finished – inspect 'cache.log' for full details")
