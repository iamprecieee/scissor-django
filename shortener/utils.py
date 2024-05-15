from random import choices
import string
from urllib.parse import urlparse
from django.forms import ValidationError
import requests
from .models import *


def generate_short_url():
    return "".join(choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=6))


def url_cleaner(url):
    # Validate URL format
    parsed_url = urlparse(url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        raise ValidationError("Enter a valid URL")
        
    # Check if URL is reachable
    try:
        requests.head(url, allow_redirects=True, timeout=5)
    except requests.exceptions.ConnectionError:
        raise ValidationError("URL is not reachable. Please enter a valid and reachable URL.")
    except requests.exceptions.Timeout:
        raise ValidationError("Process took too long and timed out. Please try again")

    return url


def check_url(url):
    if ShortUrlModel.objects.filter(short_url=url).exists():
        raise ValidationError("This short url already exists")
    if CustomUrlModel.objects.filter(custom_url=url).exists():
        raise ValidationError("This custom url already exists")
    
    return url