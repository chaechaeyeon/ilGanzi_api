from django.contrib import admin
from .models import User


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phoneNumber', 'last_login', 'treename', 'treephase', 'totalWatered', 'watered', 'tutorial', 'created_at')
