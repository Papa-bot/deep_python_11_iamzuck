import json
import random
import string
import pytest
import custom_json
# pylint: disable=c-extension-no-member


def rnd_key(max_len=8):
    return "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, max_len)))


def rnd_val(k):
    cases = [
        random.randint(-10**120, 10**120),
        k[::-1],
    ]
    return random.choice(cases)


def gen():
    d = {}
    for _ in range(200):
        k = rnd_key()
        d[k] = rnd_val(k)
    return d


@pytest.mark.parametrize("data", [gen() for _ in range(100)])
def test_roundtrip(data):
    s = custom_json.dumps(data)
    assert custom_json.loads(s) == data
    assert json.loads(s) == data
