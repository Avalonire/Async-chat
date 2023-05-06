import logging
from functools import wraps
import server_log_config
import traceback


def logged(name):
    def wrap(func):
        logger = logging.getLogger(name)

        @wraps(func)
        def wrapper(*args):
            stack = traceback.extract_stack()
            logger.debug(f'Call: {func.__name__}\n'
                         f'{" " * 43}With args: {args}\n'
                         f'{" " * 43}From: {stack[-2][2]}()')
            f = func(*args)
            return f

        return wrapper

    return wrap
