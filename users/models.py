
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import (
    validate_username,
    validate_email_regex,
    validate_phone_number,
)


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[validate_username],
    )

    email = models.EmailField(
        unique=True,
        validators=[validate_email_regex],
    )

    phone_number = models.CharField(
        max_length=16,
        blank=True,
        validators=[validate_phone_number],
    )

    def __str__(self):
        return self.username
