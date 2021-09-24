import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from libs.models import TimeStampModel
from .model_managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, TimeStampModel):
    """User model class"""

    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=250, unique=True)
    phone_number = models.CharField(max_length=50, null=True, unique=True)
    id_number = models.CharField(max_length=50, null=True, unique=True)
    profile_picture = models.ImageField(blank=True, upload_to="profile_pictures")
    should_set_password = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email


def generate_password():
    """Generate an 8 digits default password for user"""

    list = [random.choice(range(0, 9)) for i in range(0, 8)]
    password = "".join(str(i) for i in list)
    return password
