"""
Different decorators
"""
import time


def sec_time_sleep(func):
    """

    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        time.sleep(1)
        return func(*args, **kwargs)
    return wrapper


def select_time_sleep(sec=1):
    """

    :param sec:
    :return:
    """
    def time_sleep(func):
        """

        :param func:
        :return:
        """
        def wrapper(*args, **kwargs):
            """

            :param args:
            :param kwargs:
            :return:
            """
            time.sleep(sec)
            return func(*args, **kwargs)
        return wrapper
    return time_sleep


def function_duration(func):
    """

    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        start = time.perf_counter()
        run = func(*args, **kwargs)
        finish = time.perf_counter() - start
        duration = finish - start
        print('Function "{}()" duration is {:0.6f} sec'.format(func.__name__, duration))
        return run
    return wrapper


def function_arguments(func):
    """

    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        if args:
            print('args of "{}()":'.format(func.__name__))
            for i in args:
                print(i)
        if kwargs:
            print('kwargs of "{}()":'.format(func.__name__))
            for key in kwargs:
                print('{} - {}'.format(key, kwargs[key]))
        return func(*args, **kwargs)
    return wrapper
