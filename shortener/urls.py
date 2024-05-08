from django.urls import path
from .views import *


app_name = "shortener"

urlpatterns = [
    path("", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("shorten/", shorten, name="shorten")
]