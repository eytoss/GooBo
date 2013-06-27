from django.db import models


class Jiyi(models.Model):
    """
        Store the mapping information from a short hint to the real message
    """
    hint = models.CharField(max_length=50, db_index=True, unique=True)
    message = models.CharField(max_length=500)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)


class Record(models.Model):
    """
        Store the interested IRC messages in database
    """
    keyword = models.CharField(max_length=200, db_index=True,
                               help_text="keyword which triggered recording")
    sender = models.CharField(max_length=200)
    recipient = models.CharField(max_length=200)
    message = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)


class AutoReply(models.Model):
    """
        Auto reply predefined message if keyword is detected
    """
    keyword = models.CharField(max_length=200, db_index=True,
                               help_text="which will trigger auto-reply")
    msg_cnt_dn = models.CharField(max_length=500,
                                  help_text="message during count-down")
    msg = models.CharField(max_length=500,
                           help_text="message after count-down")
    count_down = models.IntegerField(blank=True, null=True, help_text=
                                     "Count down time in minutes")
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
