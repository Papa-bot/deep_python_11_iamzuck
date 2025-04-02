import json
from typing import Callable


def process_json(
    json_str: str,
    required_keys: list[str] | None = None,
    tokens: list[str] | None = None,
    callback: Callable[[str, str], None] | None = None,
) -> None:
    if not isinstance(json_str, str):
        raise TypeError("json_str must be a string")

    if required_keys is not None and not all(isinstance(key, str) for key in required_keys):
        raise TypeError("All required_keys must be strings")

    if tokens is not None and not all(isinstance(token, str) for token in tokens):
        raise TypeError("All tokens must be strings")

    if callback is not None and not callable(callback):
        raise TypeError("callback must be callable")

    if required_keys is None or tokens is None or callback is None:
        return

    data = json.loads(json_str)
    token_set = set(token.upper() for token in tokens)

    for key, value in data.items():
        if key in required_keys:
            input_tokens = value.split()
            for input_token in input_tokens:
                if input_token.upper() in token_set:
                    callback(key, input_token)


if __name__ == "__main__":
    EXAMPLE_JSON_STR = '{"key1": "Word1 word2", "key2": "word2 word3"}'
    EXAMPLE_REQUIRED_KEYS = ["key1", "KEY2"]
    EXAMPLE_TOKEN = ["WORD1", "word2"]

    def func(key, token):
        print(f'{key=}, {token=}')

    process_json(EXAMPLE_JSON_STR, EXAMPLE_REQUIRED_KEYS, EXAMPLE_TOKEN, func)
