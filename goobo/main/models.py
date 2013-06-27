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
