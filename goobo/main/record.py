"""
hint.py - Hint Module
"""
import datetime
import pytz
from django.conf import settings
from django.db import IntegrityError
from main.module import command
from main.models import Record

CMD_STR = "history"
LOCAL_TZ = pytz.timezone(settings.TIME_ZONE)


@command(CMD_STR)
def record(goobo, reply_to, command_str):
    """
        Given a keyword, return the recorded IRC messages in Record model
    """
    # usage note.
    if not command_str:
        goobo.say(reply_to, "{}{} <keyword> For example: {}{} dev2"
                  .format(settings.COMMAND_PREFIX, CMD_STR,
                          settings.COMMAND_PREFIX, CMD_STR))
        return
    # query hint
    keyword = command_str
    records = Record.objects.filter(keyword=keyword)
    for rec in records:
        local_dt = rec.date_created.astimezone(LOCAL_TZ)
        say_str = u"{} ({}) {}".format(local_dt.strftime("%H:%M"),
                                       rec.sender, rec.message)
        goobo.say(reply_to, say_str, delay=0.2)
