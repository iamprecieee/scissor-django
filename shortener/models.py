from django.db.models import (Model, UUIDField, URLField, CharField,
                              DateTimeField, IntegerField, ForeignKey, CASCADE)
from uuid import uuid4
from django.conf import settings

# Model for short url
class ShortUrlModel(Model):
    id = UUIDField(primary_key=True, editable=False, default=uuid4)
    original_url = URLField(max_length=500, null=False, blank=False)
    short_url = CharField(max_length=120, unique=True, null=False)
    click_count = IntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)
    user = ForeignKey(settings.AUTH_USER_MODEL, related_name="shortened_urls", on_delete=CASCADE)
    
    class Meta:
        ordering = ["-created_at"]
        
    def __str__(self):
        return str(self.id)
    

class CustomUrlModel(Model):
    id = UUIDField(primary_key=True, editable=False, default=uuid4)
    original_url = URLField(max_length=500, blank=False)
    custom_url = CharField(max_length=120, unique=True, blank=False)
    click_count = IntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)
    user = ForeignKey(settings.AUTH_USER_MODEL, related_name="custom_shortened_urls", on_delete=CASCADE)
    
    class Meta:
        ordering = ["-created_at"]
        
    def __str__(self):
        return str(self.id)