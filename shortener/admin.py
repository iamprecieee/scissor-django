from django.contrib.admin import ModelAdmin, register
from .models import *


# Short url model
@register(ShortUrlModel)
class ShortUrlAdmin(ModelAdmin):
    list_display = ("id", "original_url", "short_url", "created_at")
    
    
# Custom url model
@register(CustomUrlModel)
class CustomUrlAdmin(ModelAdmin):
    list_display = ("id", "original_url", "custom_url", "created_at")