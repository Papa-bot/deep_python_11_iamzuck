import abc
# pylint: disable=too-few-public-methods


class Base(abc.ABC):
    def __set_name__(self, owner, name):
        self.private_name = '_' + name  # pylint: disable=attribute-defined-outside-init

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name, None)

    def __set__(self, instance, value):
        self.check_value(value)
        setattr(instance, self.private_name, value)

    @abc.abstractmethod
    def check_value(self, value):
        pass


class Integer(Base):
    def check_value(self, value):
        if not isinstance(value, int):
            raise TypeError(f"Значение {value} должно быть int, а не {type(value).__name__}")


class String(Base):
    def check_value(self, value):
        if not isinstance(value, str):
            raise TypeError(f"Значение {value} должно быть str, а не {type(value).__name__}")


class PositiveInteger(Base):
    def check_value(self, value):
        if not isinstance(value, int):
            raise TypeError(f"Значение {value} должно быть int, а не {type(value).__name__}")
        if value <= 0:
            raise ValueError(f"Значение {value} должно быть положительным ( > 0 )")


class Data:
    num = Integer()
    name = String()
    price = PositiveInteger()

    def __init__(self, num, name, price):
        self.num = num
        self.name = name
        self.price = price
