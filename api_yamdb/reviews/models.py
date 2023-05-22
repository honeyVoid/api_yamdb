from django.contrib.auth.models import AbstractUser
from django.db import models

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
ROLES = [
    (ADMIN, 'Administrator'),
    (MODERATOR, 'Moderator'),
    (USER, 'User'),
]


class User(AbstractUser):
    email = models.EmailField('email address', blank=True, unique=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        default='user',
        max_length=16,
        blank=True,
        choices=ROLES
    )

    @property
    def is_admin(self):
        if self.role == ADMIN:
            return True

    @property
    def is_moderator(self):
        if self.role == MODERATOR:
            return True
