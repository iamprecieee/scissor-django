from django.shortcuts import render
from .forms import (UserRegistrationForm, UserModel, UserLoginForm, UserPasswordEditForm,
                     UserSocialPasswordEditForm)
from django.http import HttpResponseRedirect
from django.db.transaction import atomic
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password


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


@login_required
def edit_password(request):
    user = request.user
    if not user.has_usable_password(): 
        if request.method == "POST":
            form = UserSocialPasswordEditForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data["password1"]
                user.set_password(password)
                
                with atomic():
                    user.save()

                return HttpResponseRedirect("/dashboard/")

            return render(request, "edit_password.html", {"form": form})

        form = UserSocialPasswordEditForm()
        return render(request, "edit_password.html", {"form": form})
    
    else:
        if request.method == "POST":
            form = UserPasswordEditForm(request.POST)
            if form.is_valid():
                if check_password(form.cleaned_data["password1"], user.password):
                    password = form.cleaned_data["password2"]
                    user.set_password(password)
                    
                    with atomic():
                        user.save()

                    return HttpResponseRedirect("/dashboard/")
                
                form.add_error(None, "Incorrect password detected.")

            return render(request, "edit_password.html", {"form": form})

        form = UserPasswordEditForm()
        return render(request, "edit_password.html", {"form": form})

