"""
auto replay
"""
import datetime
import pytz
import time
from django.conf import settings
from main.models import AutoReply, Record
from main.module import ex

LOCAL_TZ = pytz.timezone(settings.TIME_ZONE)

@ex
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

    for keyword in settings.LISTEN_KEYWORDS:
        if keyword in message:
            goobo.say(recipient, "Command List: {}help".
                      format(settings.COMMAND_PREFIX))

    def get_min_diff(dt_1, dt_2):
        """get the minute difference from (dt_1 - dt_2)"""
        d1_ts = time.mktime(dt_1.timetuple())
        d2_ts = time.mktime(dt_2.timetuple())
        return int((d1_ts - d2_ts) / 60)

    auto_replys = AutoReply.objects.filter(is_active=True)
    for auto_reply in auto_replys:
        if auto_reply.keyword in message:
            now = datetime.datetime.now()
            min_diff = get_min_diff(now, auto_reply.
                                    date_modified.astimezone(LOCAL_TZ))
            if auto_reply.count_down and min_diff < auto_reply.count_down:
                message = auto_reply.msg_cnt_dn.\
                    format(auto_reply.count_down - min_diff)
            else:
                message = auto_reply.msg
            goobo.say(recipient, message)
