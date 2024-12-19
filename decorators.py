import pickle
import time
from functools import wraps

from redis.asyncio import Redis

from settings import settings

redis = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
    password=settings.redis_password
)

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
        @wraps(func)
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


def cached_result_decorator(expiry: int = None):
    """
    A decorator to cache function results in Redis.

    Args:
        expiry (int, optional): Cache expiry time in seconds. Defaults to None (no expiry).

    Returns:
        function: A wrapped function with caching.

    Usage:
        @cached_result_decorator(expiry=3600)
        def some_function(arg1, arg2):
            # Function logic here
            pass
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate a unique cache key based on function name and arguments
            cache_key = f"{func.__name__}:{pickle.dumps((args, tuple(kwargs.items())))}"

            try:
                # Check if result exists in Redis
                cached_result = await redis.get(cache_key)
                if cached_result is not None:
                    print(f'Redis Cache Hit for key {cache_key}')
                    return pickle.loads(cached_result)

                # Execute the function and cache the result
                result = func(*args, **kwargs)
                await redis.set(cache_key, pickle.dumps(result), ex=expiry)
                return result
            except Exception as error:
                raise Exception(f"Error during caching operation: {error}") from error

        return wrapper
    return decorator