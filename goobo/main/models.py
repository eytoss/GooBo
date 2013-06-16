from django.db import models


class Jiyi(models.Model):
    """
        Store the mapping information from a short hint to the real message
    """
    hint = models.CharField(max_length=50, db_index=True, unique=True)
    message = models.CharField(max_length=500)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
