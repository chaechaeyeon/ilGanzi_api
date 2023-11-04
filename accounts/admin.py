from django.contrib import admin
from .models import User


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'last_login', 'treename', 'treephase', 'watered', 'tutorial', 'created_at', 'updated_at')
