from django.forms import ModelForm, ValidationError
from .models import *


# Form for short url
class ShortenUrlForm(ModelForm):
    class Meta:
        model = ShortUrlModel
        fields = ["original_url", "short_url"]
        
    def clean_short_url(self):
        existing_url = self.cleaned_data["short_url"]
        if ShortUrlModel.objects.filter(short_url=existing_url).exists():
            raise ValidationError("This short URL already exists!")
        return existing_url
        
        