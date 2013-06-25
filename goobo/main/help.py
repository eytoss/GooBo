"""
help.py
"""
from django.conf import settings
from main.module import command

CP = settings.COMMAND_PREFIX


@command("help")
def help(reply_to, command_str):
    """
        help messaging if invalid command is received.
    """
    goobo.send_message(reply_to, "Command List: \
            {}hint {}txt {}email".format(CP, CP, CP)),
