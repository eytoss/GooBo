"""
auto replay
"""
from django.conf import settings


def keyword_react(goobo, channel, message):
    """
        react upon listened any keywords in LISTEN_KEYWORDS
    """
    for name in settings.AUTO_REPLY_KEYWORDS:
        if name in message:
            goobo.say(channel, "{name} is currently not available."
                         .format(name=name))
            return
    for keyword in settings.LISTEN_KEYWORDS:
        if keyword in message:
            goobo.say(channel, "Command List: {}help".
                         format(settings.COMMAND_PREFIX))
