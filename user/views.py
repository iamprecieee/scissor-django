from django.shortcuts import render
from .forms import UserRegistrationForm, UserModel, UserLoginForm
from django.http import HttpResponseRedirect
from django.db.transaction import atomic
from django.contrib.auth import authenticate, login
from django.db.models import Q


def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            
            with atomic():
                UserModel.objects.create_user(email=email, password=password, username=username)

            return HttpResponseRedirect("/login/")

        return render(request, "register.html", {"form": form})

    form = UserRegistrationForm()
    return render(request, "register.html", {"form": form})


def login_user(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email_name = form.cleaned_data["email_name"]
            password = form.cleaned_data["password"]
            user = UserModel.objects.filter(
                Q(email=email_name) | Q(username=email_name)
            ).first()
            
            user = authenticate(request,
                username=user.email,
                password=password
            )
            
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect("/dashboard/")
                
                form.add_error(None, "Inactive user account detected.")
            
            form.add_error(None, "Invalid login credentials.")
        
        return render(request, "login.html", {"form": form})
    
    form = UserLoginForm()
    return render(request, "login.html", {"form": form})