import re
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .error_messages import errors


class UserManager(BaseUserManager):
    """Custom user manager"""

    def validate_email(self, email):
        """Validate user email"""

        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(errors["email"]["invalid"])

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a user"""

        if email:
            email = self.normalize_email(email)
            self.validate_email(email)

        else:
            raise ValueError(errors["email"]["required"])

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.is_staff = False
        user.is_admin = False
        user.is_superuser = False
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a superuser"""

        user = self.create_user(email, password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
