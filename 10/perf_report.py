import json
import time
import random
import string
import statistics as st
import custom_json


def big(n=200_000):
    d = {}
    for _ in range(n):
        k = "".join(random.choices(string.ascii_letters, k=8))
        d[k] = random.randint(0, 1_000_000) if random.random() < 0.5 else k[::-1]
    return d


data = big()


def bench(fn, arg, repeat=5):
    times = []
    for _ in range(repeat):
        t0 = time.perf_counter()
        fn(arg)
        times.append(time.perf_counter() - t0)
    return st.mean(times), st.stdev(times)


dj, sdj = bench(json.dumps,  data)
dc, sdc = bench(custom_json.dumps, data)
lj, slj = bench(json.loads,  json.dumps(data))
lc, slc = bench(custom_json.loads, json.dumps(data))

print("\n--- Performance report (mean ± stdev, sec) ---")
print(f" dumps: stdlib {dj:.4f} ±{sdj:.4f} | custom {dc:.4f} ±{sdc:.4f}  -> {dc/dj*100:.1f}%")
print(f" loads: stdlib {lj:.4f} ±{slj:.4f} | custom {lc:.4f} ±{slc:.4f}  -> {lc/lj*100:.1f}%")
