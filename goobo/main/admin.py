from django.contrib import admin
from main.models import Jiyi, Record


class JiyiAdmin(admin.ModelAdmin):
    search_fields = ["hint", "message", ]
    ordering = ["hint", ]
    list_display = ["hint", "message", "date_created", "date_modified"]
    date_hierarchy = "date_modified"
    list_filter = ("date_modified", )

admin.site.register(Jiyi, JiyiAdmin)


class RecordAdmin(admin.ModelAdmin):
    search_fields = ["keyword", "message", ]
    ordering = ["keyword", ]
    list_display = ["keyword", "sender", "recipient",
                    "message", "date_created"]
    date_hierarchy = "date_created"
    list_filter = ("date_created", )

admin.site.register(Record, RecordAdmin)
