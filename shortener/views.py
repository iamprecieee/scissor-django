from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.conf import settings
from django.http import HttpResponseRedirect
from .utils import *


def home(request):
    return render(request, "home.html")

def dashboard(request):
    urls = ShortUrlModel.objects.all()
    custom_urls = CustomUrlModel.objects.all()
    return render(request, "dashboard.html", {"urls": urls, "custom_urls": custom_urls, "server_name": settings.SERVER_NAME})

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
                
            # Create and save URLs
            new_url = ShortUrlModel.objects.create(short_url=short_url, **form.cleaned_data)
            new_url.save()
            return HttpResponseRedirect("/dashboard/")
        
        return render(request, "shortener/short_url.html",
                  {"form": form})
    
    form = ShortenUrlForm()
    return render(request, "shortener/short_url.html",
                  {"form": form})
    
def custom_shorten(request):
    if request.method == "POST":
        form = CustomUrlForm(request.POST)
        if form.is_valid():
            # Create and save URLs
            new_url = CustomUrlModel.objects.create(**form.cleaned_data)
            new_url.save()
            return HttpResponseRedirect("/dashboard/")
        
        return render(request, "shortener/custom_url.html",
                  {"form": form})
        
    form = CustomUrlForm()
    return render(request, "shortener/custom_url.html",
                  {"form": form})
        
def redirection(request, url):
    short_url = ShortUrlModel.objects.filter(short_url=url).first()
    custom_url = CustomUrlModel.objects.filter(custom_url=url).first()
    if not (short_url, custom_url):
        return HttpResponseRedirect("/dashboard/")
    
    try:
        return redirect(short_url.original_url)
    except:
        return redirect(custom_url.original_url)
    