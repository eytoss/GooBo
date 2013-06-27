"""
auto replay
"""
from django.conf import settings
from main.models import Record


def keyword_react(goobo, sender, recipient, message):
    """
        react upon listened any keywords in LISTEN_KEYWORDS
    """
    for keyword in settings.AUTO_RECORD_KEYWORDS:
        if keyword in message:
            record = Record()
            record.keyword = keyword
            record.sender = sender
            record.recipient = recipient
            record.message = message
            record.save()
    for keyword in settings.AUTO_REPLY_KEYWORDS:
        if keyword in message:
            goobo.say(recipient, "{keyword} is currently not available."
                      .format(keyword=keyword))
            return
    for keyword in settings.LISTEN_KEYWORDS:
        if keyword in message:
            goobo.say(recipient, "Command List: {}help".
                      format(settings.COMMAND_PREFIX))
