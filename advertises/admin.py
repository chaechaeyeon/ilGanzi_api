from django.contrib import admin
from .models import Advertise

@admin.register(Advertise)
class CodeForFindPwModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'adimage', 'adname', 'brandDetail', 'adurl')