from django.forms import (ModelForm, CharField, PasswordInput, ValidationError,
                           Form, EmailInput)
from .models import UserModel
from django.db.models import Q


# Form for user registration
class UserRegistrationForm(ModelForm):
    password1 = CharField(label="Enter Password", widget=PasswordInput)
    password2 = CharField(label="Repeat Password", widget=PasswordInput)
    
    class Meta:
        model = UserModel
        fields = ["email", "username"]
        
    def clean_password2(self):
        cleaned_form_data = self.cleaned_data
        if cleaned_form_data["password1"] != cleaned_form_data["password2"]:
            raise ValidationError("Passwords do not match")
        
        return cleaned_form_data["password2"]
    
    def clean_email(self):
        cleaned_form_data = self.cleaned_data
        if UserModel.objects.filter(email=cleaned_form_data["email"]).exists():
            raise ValidationError("A user with this email already exists.")
        
        return cleaned_form_data["email"]
    
    def clean_username(self):
        cleaned_form_data = self.cleaned_data
        if UserModel.objects.filter(username=cleaned_form_data["username"]).exists():
            raise ValidationError("A user with this username already exists.")
        
        return cleaned_form_data["username"]
    
    
class UserLoginForm(Form):
    email_name = CharField(label="Enter Email/Username")
    password = CharField(label="Enter Password", widget=PasswordInput)
    
    def clean_email_name(self):
        email_name = self.cleaned_data["email_name"]
        if not UserModel.objects.filter(
            Q(email=email_name) | Q(username=email_name)
        ).exists():
            raise ValidationError("Invalid email/username.")
        
        return email_name
    
    
class UserPasswordEditForm(Form):
    password1 = CharField(label="Enter Old Password", widget=PasswordInput)
    password2 = CharField(label="Enter New Password", widget=PasswordInput)
    password3 = CharField(label="Repeat New Password", widget=PasswordInput)
    
    def clean_password3(self):
        cleaned_form_data = self.cleaned_data
        if cleaned_form_data["password2"] != cleaned_form_data["password3"]:
            raise ValidationError("Passwords do not match")
        
        return cleaned_form_data["password2"]
    
    
class UserSocialPasswordEditForm(Form):
    password1 = CharField(label="Enter Password", widget=PasswordInput)
    password2 = CharField(label="Repeat Password", widget=PasswordInput)
    
    def clean_password2(self):
        cleaned_form_data = self.cleaned_data
        if cleaned_form_data["password1"] != cleaned_form_data["password2"]:
            raise ValidationError("Passwords do not match")
        
        return cleaned_form_data["password2"]
    
    
class PasswordResetRequestForm(Form):
    email = CharField(label="Enter Email", widget=EmailInput)
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        if not UserModel.objects.filter(email=email).exists():
            raise ValidationError("Invalid email address")
        
        return email
    
    
class PasswordChangeForm(UserSocialPasswordEditForm):
    password1 = CharField(label="Enter New Password", widget=PasswordInput)