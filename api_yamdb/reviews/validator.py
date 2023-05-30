from django.core.exceptions import ValidationError
from django.utils import timezone


def yaer_validator(value):
    if value > timezone.now().year:
        raise ValidationError(
            ('Год не моожет быть больше текущего.'),
            params={'value': value},
        )
