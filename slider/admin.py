from django.contrib import admin
from . import models

@admin.register(models.Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'image']
    search_fields = ['title', 'url']