from django.forms import ModelForm, ValidationError
from .models import *
from urllib.parse import urlparse
import requests


# Form for short url
class ShortenUrlForm(ModelForm):
    class Meta:
        model = ShortUrlModel
        fields = ["original_url"]
        
    def clean_original_url(self):
        url = self.cleaned_data["original_url"]
        
        # Validate URL format
        parsed_url = urlparse(url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValidationError("Enter a valid URL")
        
        # Check if URL is reachable
        try:
            requests.get(url, allow_redirects=True)
        except requests.exceptions.ConnectionError:
            raise ValidationError("URL is not reachable. Please enter a valid and reachable URL.")

        return url