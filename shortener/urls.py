from django.urls import path
from .views import *


app_name = "shortener"

urlpatterns = [
    path("", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("shorten/", shorten, name="shorten"),
    path("custom-shorten/", custom_shorten, name="custom-shorten"),
    path("<str:url>/", redirection, name="redirection"),
    path("generate-qr/<str:url>/", generate_qrcode, name="generate-qr-code")
]