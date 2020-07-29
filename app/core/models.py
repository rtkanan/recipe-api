from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
# from django.conf import settings


class UserManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, password=None, **kwargs):
        """Create new user profile"""
        if not email:
            raise ValueError("User must have an email address")

        # This makes the second half(domain) of the email lower case always
        email = self.normalize_email(email)

        user = self.model(email=email, **kwargs)
        user.set_password(password)

        # 'using' helps to support multiple databases
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create new superuser"""
        user = self.create_user(email, password)

        user.is_superuser = True
        user.is_staff = True

        # 'using' helps to support multiple databases
        user.save(using=self._db)

        return user


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, default='None')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Model Manager
    objects = UserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['name']

#     def get_full_name(self):
#         """Retrieve full name of the user"""
#         return self.name

#     def get_short_name(self):
#         """Retrieve short name of the user"""
#         return self.name

#     def __str__(self):
#         """Return string representation of the user"""
#         return self.email

# class ProfileFeedItem(models.Model):
#     """Profile status update"""
#     user_profile = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE
#     )
#     status_text = models.CharField(max_length=255)
#     created_on = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         """Return the model as a string"""
#         return self.status_text
