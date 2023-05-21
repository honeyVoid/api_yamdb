from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class User(AbstractUser):
    email = models.EmailField('email address', blank=True, unique=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=16, blank=True, choices=ROLE)
