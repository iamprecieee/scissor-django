from django.contrib.admin import ModelAdmin, register
from .models import UserModel


@register(UserModel)
class UserAdmin(ModelAdmin):
    list_display = ["id", "email", "username", "created_at"]