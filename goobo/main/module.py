"""
    support dynamically load modules
"""


def command(value):
    """
        add command attribute to the callable
        to make it a goobo module
    """
    def add_command(func):
        func.command = value
        return func
    return add_command


def ex(func):
    """
        exception wrapper
    """
    def _wrapped_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception, e:
            pass
    # these two lines are what makes _wrapped_func disguised as func
    _wrapped_func.__doc__ = func.__doc__
    _wrapped_func.__dict__ = func.__dict__
    return _wrapped_func
