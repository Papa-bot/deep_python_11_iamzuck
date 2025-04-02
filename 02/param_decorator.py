from functools import wraps


def retry_deco(retries=1, expected_exceptions=None):
    expected_exceptions = tuple(expected_exceptions or [])

    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            attempt = 1
            while attempt <= retries:
                try:
                    result = func(*args, **kwargs)
                    if args and kwargs:
                        print(
                            f'\nrun \"{func.__name__}\" '
                            f'with positional args = {args}, '
                            f'keyword kwargs = {kwargs}, '
                            f'attempt = {attempt}, result = {result}'
                        )
                    elif not args and kwargs:
                        print(
                            f'\nrun \"{func.__name__}\" '
                            f'with keyword kwargs = {kwargs}, '
                            f'attempt = {attempt}, result = {result}'
                        )
                    else:
                        print(
                            f'\nrun \"{func.__name__}\" '
                            f'with positional args = {args}, '
                            f'attempt = {attempt}, result = {result}'
                        )
                    return result
                except Exception as e:  # pylint: disable=broad-exception-caught
                    if args and kwargs:
                        print(
                            f'\nrun \"{func.__name__}\" '
                            f'with positional args = {args}, '
                            f'keyword kwargs = {kwargs}, '
                            f'attempt = {attempt}, exception = {type(e).__name__}'
                        )
                    elif not args and kwargs:
                        print(
                            f'\nrun \"{func.__name__}\" '
                            f'with keyword kwargs = {kwargs}, '
                            f'attempt = {attempt}, exception = {type(e).__name__}'
                        )
                    else:
                        print(
                            f'\nrun \"{func.__name__}\" '
                            f'with positional args = {args}, '
                            f'attempt = {attempt}, exception = {type(e).__name__}'
                        )

                    if isinstance(e, expected_exceptions):
                        break

                    attempt += 1
            return None
        return inner
    return decorator


if __name__ == '__main__':
    @retry_deco(3)
    def add(a, b):
        return a + b

    @retry_deco(3)
    def check_str(value=None):
        if value is None:
            raise ValueError()
        return isinstance(value, str)

    @retry_deco(2, [ValueError])
    def check_int(value=None):
        if value is None:
            raise ValueError()
        return isinstance(value, int)

    add(4, 2)
    add(4, b=3)
    add(a=13, b=14)

    check_str(value="123")
    check_str(1)
    check_str(value=None)

    check_int(value=1)
    check_int(value=None)
