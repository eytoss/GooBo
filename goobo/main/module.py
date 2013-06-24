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
