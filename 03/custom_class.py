class CustomList(list):
    def __add__(self, other):
        if isinstance(other, (list, CustomList)):
            max_len = max(len(self), len(other))
            new_list = [(self[i] if i < len(self) else 0) +
                        (other[i] if i < len(other) else 0) for i in range(max_len)]
            return CustomList(new_list)
        if isinstance(other, int):
            return CustomList([x + other for x in self])
        raise TypeError("Unsupported type for addition")

    def __radd__(self, other):
        if isinstance(other, (list, CustomList, int)):
            return self + other
        raise TypeError("Unsupported type for addition")

    def __sub__(self, other):
        if isinstance(other, (list, CustomList)):
            max_len = max(len(self), len(other))
            new_list = [(self[i] if i < len(self) else 0) -
                        (other[i] if i < len(other) else 0) for i in range(max_len)]
            return CustomList(new_list)
        if isinstance(other, int):
            return CustomList([x - other for x in self])
        raise TypeError("Unsupported type for subtraction")

    def __rsub__(self, other):
        if isinstance(other, (list, CustomList)):
            max_len = max(len(self), len(other))
            new_list = [(other[i] if i < len(other) else 0) -
                        (self[i] if i < len(self) else 0) for i in range(max_len)]
            return CustomList(new_list)
        if isinstance(other, int):
            return CustomList([other - x for x in self])
        raise TypeError("Unsupported type for subtraction")

    def __eq__(self, other):
        if isinstance(other, CustomList):
            return sum(self) == sum(other)
        raise TypeError("Unsupported type for comparison")

    def __ne__(self, other):
        if isinstance(other, CustomList):
            return sum(self) != sum(other)
        raise TypeError("Unsupported type for comparison")

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


if __name__ == '__main__':
    c1 = CustomList([5, 1, 3, 7]) + CustomList([1, 2, 7])
    print(c1)  # CustomList([6, 3, 10, 7])
    print(CustomList([10]) + [2, 5])  # CustomList([12, 5])
    print([2, 5] + CustomList([10]))  # CustomList([12, 5])
    print(CustomList([2, 5]) + 10)  # CustomList([12, 15])
    print(10 + CustomList([2, 5]))  # CustomList([12, 15])

    print(CustomList([5, 1, 3, 7]) - CustomList([1, 2, 7]))  # CustomList([4, -1, -4, 7])
    print(CustomList([10]) - [2, 5])  # CustomList([8, -5])
    print([2, 5] - CustomList([10]))  # CustomList([-8, 5])
    print(CustomList([2, 5]) - 10)  # CustomList([-8, -5])
    print(10 - CustomList([2, 5]))  # CustomList([8, 5])
