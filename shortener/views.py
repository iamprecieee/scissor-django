from django.shortcuts import render
from .models import *
from .forms import *
from django.conf import settings
from django.http import HttpResponseRedirect
from .utils import *


def home(request):
    return render(request, "home.html")

def dashboard(request):
    urls = ShortUrlModel.objects.all()
    return render(request, "dashboard.html", {"urls": urls, "server_name": settings.SERVER_NAME})

def shorten(request):
    if request.method == "POST":
        form = ShortenUrlForm(request.POST)
        if form.is_valid():
            short_url = generate_short_url()
            
            # Handle potential short_url collisions
            collisions = 0
            while ShortUrlModel.objects.filter(short_url=short_url).exists():
                collisions += 1
                short_url = generate_short_url()
                if collisions > 5:
                    form.add_error(None, "Failed to generate a unique URL after several attempts. Please try again.")
                    return render(request, "shortener/short_url.html",
                    {"form": form})
                
            # Create an save URLs
            new_url = ShortUrlModel.objects.create(short_url=short_url, **form.cleaned_data)
            new_url.save()
            return HttpResponseRedirect("/shortener/dashboard/")
        
        else:
            return render(request, "shortener/short_url.html",
                  {"form": form})
    
    else:
        form = ShortenUrlForm()
        return render(request, "shortener/short_url.html",
                  {"form": form})