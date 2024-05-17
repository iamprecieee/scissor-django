from django.forms import ModelForm
from .models import ShortUrlModel, CustomUrlModel
from .utils import url_cleaner, check_url


# Form for short url
class ShortenUrlForm(ModelForm):
    class Meta:
        model = ShortUrlModel
        fields = ["original_url"]
        
    def clean_original_url(self):
        url = self.cleaned_data["original_url"]
        return url_cleaner(url)
    

# Form for custom url
class CustomUrlForm(ModelForm):
    class Meta:
        model = CustomUrlModel
        fields = ["original_url", "custom_url"]
    
    def clean_original_url(self):
        url = self.cleaned_data["original_url"]
        return url_cleaner(url)
    
    def clean_custom_url(self):
        url = self.cleaned_data["custom_url"]
        return check_url(url)
    

# Form for editing custom url
class EditCustomUrlForm(ModelForm):
    class Meta:
        model = CustomUrlModel
        fields = ["custom_url"]
        labels = {"custom_url": "New custom url"}
        
    def clean_custom_url(self):
        url = self.cleaned_data["custom_url"]
        return check_url(url)