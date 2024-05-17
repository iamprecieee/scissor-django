from django.shortcuts import render, redirect
from .forms import (ShortUrlModel, CustomUrlModel, ShortenUrlForm, CustomUrlForm,
                    EditCustomUrlForm)
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from .utils import generate_short_url
from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_M
from io import BytesIO
from django.db.transaction import atomic
from django.contrib.auth.decorators import login_required


server_name = settings.SERVER_NAME


def home(request):
    return render(request, "home.html")


@login_required
def dashboard(request):
    user = request.user
    urls = ShortUrlModel.objects.filter(user=user).all()
    custom_urls = CustomUrlModel.objects.filter(user=user).all()
    return render(
        request,
        "dashboard.html",
        {"urls": urls, "custom_urls": custom_urls, "server_name": server_name},
    )


@login_required
def shorten(request):
    if request.method == "POST":
        form = ShortenUrlForm(request.POST)
        if form.is_valid():
            short_url = generate_short_url()
            
            # Create and save URLs
            new_url = ShortUrlModel.objects.create(
                short_url=short_url, user=request.user, **form.cleaned_data
            )
            with atomic():
                new_url.save()
                
            return HttpResponseRedirect("/dashboard/")

        return render(request, "shortener/short_url.html", {"form": form})

    form = ShortenUrlForm()
    return render(request, "shortener/short_url.html", {"form": form})


@login_required
def custom_shorten(request):
    if request.method == "POST":
        form = CustomUrlForm(request.POST)
        if form.is_valid():
            # Create and save URLs
            new_url = CustomUrlModel.objects.create(
                user=request.user, **form.cleaned_data
                )
            with atomic():
                new_url.save()
            return HttpResponseRedirect("/dashboard/")

        return render(request, "shortener/custom_url.html", {"form": form})

    form = CustomUrlForm()
    return render(request, "shortener/custom_url.html", {"form": form})


@login_required
def delete_url(request, url_id):
    if request.method == "POST":
        user = request.user
        short_url = ShortUrlModel.objects.filter(id=url_id, user=user).first()
        custom_url = CustomUrlModel.objects.filter(id=url_id, user=user).first()

        if short_url:
            with atomic():
                short_url.delete()

        if custom_url:
            with atomic():
                custom_url.delete()

        return HttpResponseRedirect("/dashboard/")


@login_required
def edit_url(request, url_id):
    if request.method == "POST":
        user = request.user
        form = EditCustomUrlForm(
            request.POST, instance=CustomUrlModel.objects.filter(id=url_id, user=user).first()
        )
        if form.is_valid():
            with atomic():
                form.save()
            return HttpResponseRedirect("/dashboard/")

        return render(request, "shortener/edit.html", {"form": form})

    form = EditCustomUrlForm()
    return render(request, "shortener/edit.html", {"form": form})


def redirection(request, url):
    short_url = ShortUrlModel.objects.filter(short_url=url).first()
    custom_url = CustomUrlModel.objects.filter(custom_url=url).first()

    if short_url:
        with atomic():
            short_url.click_count += 1
            short_url.save()
        return redirect(short_url.original_url)

    if custom_url:
        with atomic():
            custom_url.click_count += 1
            custom_url.save()
        return redirect(custom_url.original_url)

    return HttpResponseRedirect("/dashboard/")


def generate_qrcode(request, url):
    short_url = ShortUrlModel.objects.filter(short_url=url).first()
    custom_url = CustomUrlModel.objects.filter(custom_url=url).first()
    if not (short_url, custom_url):
        return HttpResponseRedirect("/dashboard/")

    qr = QRCode(
        version=2,
        error_correction=ERROR_CORRECT_M,
        box_size=5,
        border=1,
    )
    qr.add_data(server_name + "/" + url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="lime", back_color="black")
    image_buffer = BytesIO()
    img.save(image_buffer)
    image_buffer.seek(0)

    return HttpResponse(image_buffer, content_type="image/png")
