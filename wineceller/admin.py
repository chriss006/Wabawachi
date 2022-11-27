from django.contrib import admin
from .models import WineCeller


@admin.register(WineCeller)
class WinecellerAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "created_at",
        "updated_at",
    )
