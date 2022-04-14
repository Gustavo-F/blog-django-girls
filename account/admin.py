from django.contrib import admin
from . import models


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_admin', 'is_active')
    list_display_links = ('username', 'email')


admin.site.register(models.User, UserAdmin)
