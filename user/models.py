from django.db.models import (UUIDField, CharField, EmailField, BooleanField,
                              DateTimeField)
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from uuid import uuid4

class CustomUserManager(BaseUserManager):
    MAX_SUPERUSERS_ALLOWED = 1
    
    def _create_user(self, email, password=None, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        if password:
            user.set_password(password)
        else:
            # This is for social login. Users can change to a new password later.
            user.set_unusable_password()
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        
        if self.filter(is_superuser=True).count() >= self.MAX_SUPERUSERS_ALLOWED:
            raise ValueError("Superuser account limit reached")
        
        return self._create_user(email, password, **kwargs)
    
    def create_user(self, email, password=None, **kwargs):
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)
        
        return self._create_user(email, password, **kwargs)
    

# Model for user [authentication/authorization]
class UserModel(AbstractBaseUser, PermissionsMixin):
    id = UUIDField(primary_key=True, editable=False, default=uuid4)
    username = CharField(max_length=120, unique=True, blank=True)
    email = EmailField(max_length=255, unique=True)
    password = CharField(max_length=255)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True, editable=False)
    last_login = DateTimeField(auto_now=True, editable=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = "email"
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.email