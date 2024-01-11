"""
    Database models.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, super_user = False, **extra_fields):
        """Create, save and return new user"""
        
        if not email:
            raise ValueError('The Email field must be set')
        
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)

        if super_user:
            user.is_staff = True
            user.is_superuser = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):

        user = self.create_user(email, password, True)
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model overriding django inbuild models"""

    email = models.EmailField(max_length = 255, unique = True)
    name = models.CharField(max_length = 255)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = True)

    objects = UserManager()

    USERNAME_FIELD =  "email"
    
