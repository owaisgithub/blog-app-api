from django.db import models
from django.contrib.auth.models import (
                                        BaseUserManager, 
                                        AbstractBaseUser,
                                        PermissionsMixin
                                        )
from django.conf import settings
from datetime import datetime, timedelta

import jwt

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, *args, **kwargs):
        if email is None:
            raise TypeError('Users must have an email address.')
        user = self.model(email=self.normalize_email(email), *args, **kwargs)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')
        
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user



class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'Users'

    def __str__(self) -> str:
        return self.email
    

    def get_full_name(self):
        return (self.first_name + " " + self.last_name)
    
    def get_short_name(self):
        return self.last_name


class BlacklistedToken(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    token = models.CharField(max_length=255)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'BlacklistedToken'

    def __str__(self) -> str:
        return self.token
