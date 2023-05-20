from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    email = models.EmailField('email address', blank=True, unique=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=16, blank=True)
    confirmation_code = models.CharField(max_length=32, blank=True)
