import random


class SomeModel:

    def predict(self, message: str) -> float:  # pylint: disable=unused-argument
        return random.uniform(0, 1)

    def mes_len(self, message):
        return len(message)
