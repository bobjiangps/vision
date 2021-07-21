class CustomException(Exception):

    def __init__(self, msg, trace=None):
        self.msg = msg
        self.trace = trace

    def __str__(self):
        exception_msg = "Message: %s\n" % self.msg
        if self.trace is not None:
            exception_msg += "traceback:\n%s" % self.trace
        return exception_msg


class NotVisibleException(CustomException):
    pass


class TimeoutException(CustomException):
    pass
