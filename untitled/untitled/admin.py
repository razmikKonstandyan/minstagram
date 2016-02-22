from django.contrib import admin

from .models import UserPage


class CustomModelAdmin(admin.ModelAdmin):
    list_display = ["title", "time_created", "time_updated", "id"]
    search_fields = ["title"]

    class Meta:
        model = UserPage

admin.site.register(UserPage, CustomModelAdmin)
