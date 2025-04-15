from functools import wraps


def _format_log_message(func, args, kwargs, attempt, result=None, exception=None):  # pylint: disable=too-many-arguments
    message_parts = [f'\nrun "{func.__name__}"']

    if args:
        message_parts.append(f'with positional args = {args}')
    if kwargs:
        if args:
            message_parts.append(f'keyword kwargs = {kwargs}')
        else:
            message_parts.append(f'with keyword kwargs = {kwargs}')

    message_parts.append(f'attempt = {attempt}')

    if exception is not None:
        message_parts.append(f'exception = {type(exception).__name__}')
    else:
        message_parts.append(f'result = {result}')

    return ' '.join(message_parts)


def retry_deco(retries=1, expected_exceptions=None):
    if not isinstance(retries, int):
        raise TypeError("retries must be an integer")

    if retries < 0:
        raise ValueError("retries cannot be negative")

    expected_exceptions = tuple(expected_exceptions or ())

    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            last_exception = None

            for attempt in range(1, retries + 1):
                try:
                    result = func(*args, **kwargs)
                    print(_format_log_message(func, args, kwargs, attempt, result=result))
                    return result

                except expected_exceptions as e:
                    print(_format_log_message(func, args, kwargs, attempt, exception=e))
                    raise e

                except Exception as e:  # pylint: disable=broad-exception-caught
                    print(_format_log_message(func, args, kwargs, attempt, exception=e))
                    last_exception = e

            if retries == 0:
                raise ValueError("Function not attempted (retries=0)")

            if last_exception is not None:
                raise last_exception

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

    try:
        check_str(value="123")
        check_str(1)
        check_str(value=None)
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Caught expected exception: {type(e).__name__}")

    try:
        check_int(value=1)
        check_int(value=None)
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Caught expected exception: {type(e).__name__}")
