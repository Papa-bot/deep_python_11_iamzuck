import random
import string
import time
# pylint: disable=c-extension-no-member


def big():
    d = {}
    for _ in range(100_000):
        k = "".join(random.choices(string.ascii_letters, k=8))
        v = random.randint(0, 1_000_000) if random.random() < 0.5 else k[::-1]
        d[k] = v
    return d


def bench(fn, arg):
    t0 = time.perf_counter()
    fn(arg)
    return time.perf_counter() - t0
