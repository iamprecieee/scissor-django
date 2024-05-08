from django.db.models import Model, UUIDField, URLField, CharField, DateTimeField
from uuid import uuid4

# Model for short url
class ShortUrlModel(Model):
    id = UUIDField(primary_key=True, editable=False, default=uuid4)
    original_url = URLField(max_length=500, null=False, blank=False)
    short_url = CharField(max_length=120, unique=True, null=False)
    created_at = DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]
        
    def __str__(self):
        return str(self.id)