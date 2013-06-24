"""
auto replay
"""
from django.conf import settings
from main.bot import send_message


def keyword_react(channel, message):
    """
        react upon listened any keywords in LISTEN_KEYWORDS
    """
    for name in settings.AUTO_REPLY_KEYWORDS:
        if name in message:
            send_message(channel, "{name} is currently not available."
                         .format(name=name))
            return
    for keyword in settings.LISTEN_KEYWORDS:
        if keyword in message:
            send_message(channel, "Command List: {}help".
                         format(settings.COMMAND_PREFIX))
