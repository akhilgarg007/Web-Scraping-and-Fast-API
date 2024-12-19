import time
from functools import wraps


def retry_on_failure(max_attempts, retry_delay=1):
    """
    A decorator to retry a function upon failure.

    Args:
        max_attempts (int): The maximum number of attempts to retry the function.
        retry_delay (int, optional): The delay (in seconds) between retries. Defaults to 1 second.

    Returns:
        function: A wrapped function that will retry upon failure.

    Usage:
        @retry_on_failure(max_attempts=3, retry_delay=2)
        def some_function():
            # Function logic here
            pass

    Raises:
        Exception: If the function fails after the maximum number of attempts.
    """
    def decorator(func):
        @wraps(func)  # Preserves the original function's signature and metadata
        def wrapper(*args, **kwargs):
            for _ in range(max_attempts):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as error:
                    print(f"Error occurred: {error}. Retrying...")
                    time.sleep(retry_delay)
            raise Exception("Maximum attempts exceeded. Function failed.")
        return wrapper
    return decorator
