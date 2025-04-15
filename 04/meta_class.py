class CustomMeta(type):
    def __new__(mcs, name, bases, namespace):
        new_namespace = {}

        for attr_name, attr_value in namespace.items():
            if (attr_name.startswith('__') and attr_name.endswith('__')) or \
               attr_name.startswith(f'_{name}__'):
                new_namespace[attr_name] = attr_value
            else:
                new_namespace[f'custom_{attr_name}'] = attr_value

        cls = super().__new__(mcs, name, bases, new_namespace)

        original_setattr = cls.__setattr__

        def __setattr__(instance, name, value):
            if (name.startswith('__') and name.endswith('__')) or \
               name.startswith(f'_{instance.__class__.__name__}__'):
                original_setattr(instance, name, value)
            else:
                original_setattr(instance, f'custom_{name}', value)

        cls.__setattr__ = __setattr__
        return cls

    def __setattr__(cls, name, value):
        if (name.startswith('__') and name.endswith('__')) or \
           name.startswith(f'_{cls.__name__}__'):
            super().__setattr__(name, value)
        else:
            super().__setattr__(f'custom_{name}', value)


class CustomClass(metaclass=CustomMeta):
    x = 50
    _protected = "protected"
    __private = "private"  # pylint: disable=unused-private-member

    def __init__(self, val=99):
        self.val = val
        self._protected_val = "protected_val"
        self.__private_val = "private_val"  # pylint: disable=unused-private-member

    def line(self):
        return 100

    def _protected_method(self):
        return "_protected_method"

    def __private_method(self):  # pylint: disable=unused-private-member
        return "__private_method"

    def __str__(self):
        return "Custom_by_metaclass"
