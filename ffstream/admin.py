from django.contrib import admin

from .models import *


class KeyAdmin(admin.ModelAdmin):
    date_hierarchy = "modified"
    list_filter = (
        "is_live",
        "active",
        "pull",
    )
    ordering = ("-modified",)
    sortable_by = (
        "name",
        "id",
        "created",
        "modified",
        "is_live",
        "active",
        "pull",
    )
    list_display = (
        "name",
        "id",
        "created",
        "modified",
        "is_live",
        "active",
        "pull",
    )


# Register your models here.
admin.site.register(Key, KeyAdmin)
admin.site.register(Stream)
