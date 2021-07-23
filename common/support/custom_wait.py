import time
import traceback
from common.support.exceptions import NotVisibleException
from common.support.exceptions import TimeoutException


IGNORED_EXCEPTIONS = (NotVisibleException,)


class CustomWait:

    def __init__(self, driver, timeout=30, frequency=0.5, ignored_exceptions=None):
        self._driver = driver
        self._timeout = timeout
        self._frequency = frequency
        exceptions = list(IGNORED_EXCEPTIONS)
        if ignored_exceptions is not None:
            try:
                exceptions.extend(iter(ignored_exceptions))
            except TypeError:
                exceptions.append(ignored_exceptions)
        self._ignored_exceptions = tuple(exceptions)

    def until(self, method, message=""):
        end_time = time.time() + self._timeout
        trace = None
        while time.time() <= end_time:
            try:
                value = method(self._driver)
                if value:
                    return value
            except self._ignored_exceptions:
                trace = str(traceback.format_exc())
            time.sleep(self._frequency)
        raise TimeoutException(message, trace)

    def until_not(self, method, message=""):
        end_time = time.time() + self._timeout
        while time.time() <= end_time:
            try:
                value = method(self._driver)
                if not value:
                    return value
            except self._ignored_exceptions:
                return True
            time.sleep(self._frequency)
        raise TimeoutException(message)
