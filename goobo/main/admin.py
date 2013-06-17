from django.contrib import admin
from main.models import Jiyi


class JiyiAdmin(admin.ModelAdmin):
    search_fields = ["hint", "message",]
    ordering = ["hint",]
    list_display = ["hint", "message", "date_created", "date_modified"]
    date_hierarchy = "date_modified"
    list_filter = ("date_modified",)

admin.site.register(Jiyi, JiyiAdmin)
