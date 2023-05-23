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
    email = models.EmailField('email address', blank=False, unique=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        default=USER,
        max_length=50,
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
