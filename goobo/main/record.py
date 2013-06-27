"""
hint.py - Hint Module
"""
import pytz
from django.conf import settings
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
        goobo.say(reply_to, "{}{} <keyword> For example: {}{} my_nick"
                  .format(settings.COMMAND_PREFIX, CMD_STR,
                          settings.COMMAND_PREFIX, CMD_STR))
        return
    # query hint
    cmd_parts = command_str.split()
    keyword = cmd_parts[0]

    number = 3
    dt_format = "0"
    if len(cmd_parts) > 1:
        number = cmd_parts[1]
    if len(cmd_parts) > 2:
        dt_format = cmd_parts[2]

    records = Record.objects.filter(keyword=keyword)\
        .order_by("-date_created")[:number]
    for rec in records:
        local_dt = rec.date_created.astimezone(LOCAL_TZ)
        if dt_format == "1":
            local_dt_str = local_dt.strftime("%b %d %H:%M")
        else:
            local_dt_str = local_dt.strftime("%H:%M")
        say_str = u"{} ({}) {}".format(local_dt_str,
                                       rec.sender, rec.message)
        goobo.say(reply_to, say_str, delay=0.2)
