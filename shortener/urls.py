from django.urls import path
from .views import (home, dashboard, shorten, custom_shorten,
                    delete_url, edit_url, redirection, generate_qrcode)


app_name = "shortener"

urlpatterns = [
    path("", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("shorten/", shorten, name="shorten"),
    path("custom-shorten/", custom_shorten, name="custom-shorten"),
    path("delete/<uuid:url_id>/", delete_url, name="delete"),
    path("edit/<uuid:url_id>/", edit_url, name="edit"),
    path("<str:url>/", redirection, name="redirection"),
    path("generate-qr/<str:url>/", generate_qrcode, name="generate-qr-code")
]