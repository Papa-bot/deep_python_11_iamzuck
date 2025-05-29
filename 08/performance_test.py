# pylint: disable=too-few-public-methods
# pylint: disable=redefined-outer-name
import time
import weakref
import gc


class RegularClass:
    def __init__(self, a, b) -> None:
        self.a = a
        self.b = b


class SlottedClass:
    __slots__ = ("a", "b")

    def __init__(self, a, b) -> None:
        self.a = a
        self.b = b


class DataHolder:
    def __init__(self, data):
        self.data = data


class WeakRefClass:
    def __init__(self, a, b) -> None:
        self.ref_a = weakref.ref(a)
        self.ref_b = weakref.ref(b)

    @property
    def a_value(self):
        return self.ref_a()

    @a_value.setter
    def a_value(self, v):
        self.ref_a = weakref.ref(v)


def benchmark(cls, num_objs: int):
    gc.disable()
    data_objects = [DataHolder(i) for i in range(num_objs)]

    start = time.perf_counter()
    instances = [cls(data_objects[i], data_objects[i]) for i in range(num_objs)]
    create_time = time.perf_counter() - start

    start = time.perf_counter()
    total = 0
    for inst in instances:
        if cls is WeakRefClass:
            total += inst.a_value.data
        else:
            total += inst.a.data
    read_time = time.perf_counter() - start

    start = time.perf_counter()
    new_val = DataHolder(total)
    for inst in instances:
        if cls is WeakRefClass:
            inst.a_value = new_val
        else:
            inst.a = new_val
    write_time = time.perf_counter() - start

    gc.enable()
    return create_time, read_time, write_time


if __name__ == "__main__":
    NUM_OBJECTS = 1_000_000
    for cls in (RegularClass, SlottedClass, WeakRefClass):
        create, read, write = benchmark(cls, NUM_OBJECTS)
        print(
            f"{cls.__name__:>12}  "
            f"create={create:.4f}s  "
            f"read={read:.4f}s  "
            f"write={write:.4f}s"
        )
