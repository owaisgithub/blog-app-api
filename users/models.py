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
    handle = models.CharField(max_length=50, null=True, blank=True, unique=True)
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
    

    def getFullName(self):
        return (self.first_name + " " + self.last_name)
    
    def get_short_name(self):
        return self.last_name

    @classmethod
    def getUserById(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
        
    @classmethod
    def getUserByHandle(self, handle):
        try:
            return User.objects.get(handle=handle)
        except:
            return None


class UserImage(models.Model):
    image = models.ImageField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile_image")

    class Meta:
        db_table = 'UserImage'

    def __str__(self):
        return self.user.email + " Profile Image"


class UserDetail(models.Model):
    dob = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_detail')


    class Meta:
        db_table = 'UserDetail'


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Follows'

    @classmethod
    def getFollow(self, data):
        try:
            return Follow.objects.filter(follower=data['follower'], following=data['following'])
        except Follow.DoesNotExist:
            return None


class BlacklistedToken(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    token = models.CharField(max_length=255)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'BlacklistedToken'

    def __str__(self) -> str:
        return self.token
