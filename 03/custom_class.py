from itertools import zip_longest


class CustomList(list):
    def __add__(self, other):
        if isinstance(other, (list, CustomList)):
            new_list = [x + y for x, y in zip_longest(self, other, fillvalue=0)]
            return CustomList(new_list)
        if isinstance(other, int):
            return CustomList([x + other for x in self])
        raise TypeError("Unsupported type for addition")

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, (list, CustomList)):
            new_list = [x - y for x, y in zip_longest(self, other, fillvalue=0)]
            return CustomList(new_list)
        if isinstance(other, int):
            return CustomList([x - other for x in self])
        raise TypeError("Unsupported type for subtraction")

    def __rsub__(self, other):
        if isinstance(other, (list, CustomList)):
            new_list = [y - x for x, y in zip_longest(self, other, fillvalue=0)]
            return CustomList(new_list)
        if isinstance(other, int):
            return CustomList([other - x for x in self])
        raise TypeError("Unsupported type for subtraction")

    def __eq__(self, other):
        if isinstance(other, CustomList):
            return sum(self) == sum(other)
        raise TypeError("Unsupported type for comparison")

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if isinstance(other, CustomList):
            return sum(self) < sum(other)
        raise TypeError("Unsupported type for comparison")

    def __le__(self, other):
        if isinstance(other, CustomList):
            return sum(self) <= sum(other)
        raise TypeError("Unsupported type for comparison")

    def __gt__(self, other):
        if isinstance(other, CustomList):
            return sum(self) > sum(other)
        raise TypeError("Unsupported type for comparison")

    def __ge__(self, other):
        if isinstance(other, CustomList):
            return sum(self) >= sum(other)
        raise TypeError("Unsupported type for comparison")

    def __str__(self):
        return f'CustomList({super().__str__()}), sum: {sum(self)}'
