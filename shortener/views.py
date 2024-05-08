from django.shortcuts import render
from .models import *
from .forms import *
from django.conf import settings
from django.http import HttpResponseRedirect


def home(request):
    return render(request, "home.html")

def dashboard(request):
    urls = ShortUrlModel.objects.all()
    return render(request, "dashboard.html", {"urls": urls, "server_name": settings.SERVER_NAME})

def shorten(request):
    if request.method == "POST":
        form = ShortenUrlForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/shortener/dashboard/")
        else:
            return render(request, "shortener/short_url.html",
                  {"form": form})
    
    else:
        form = ShortenUrlForm()
        return render(request, "shortener/short_url.html",
                  {"form": form})