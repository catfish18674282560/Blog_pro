from django.contrib import admin
from .models import ReadNum, ReadDateNum


@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'read_num')


@admin.register(ReadDateNum)
class ReadDateNumAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'date', 'read_num')
