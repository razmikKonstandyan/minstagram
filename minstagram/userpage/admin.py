from django.contrib import admin

from .models import UserPageData, UserProfileData


class CustomModelAdmin(admin.ModelAdmin):
    list_display = ["title", "time_created", "time_updated", "id"]
    search_fields = ["title"]

    class Meta:
        model = UserPageData

admin.site.register(UserPageData, CustomModelAdmin)
admin.site.register(UserProfileData)
