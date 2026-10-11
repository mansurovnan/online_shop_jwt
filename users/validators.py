
import re

from django.core.exceptions import ValidationError


USERNAME_REGEX = r"^[A-Za-z0-9_]{3,30}$"
EMAIL_REGEX = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
PHONE_REGEX = r"^\+?[0-9]{9,15}$"


def validate_username(value):
    if not re.fullmatch(USERNAME_REGEX, value):
        raise ValidationError(
            "Username 3-30 ta belgidan iborat bo'lishi kerak. "
            "Faqat harflar, raqamlar va _ ishlatish mumkin."
        )


def validate_email_regex(value):
    if not re.fullmatch(EMAIL_REGEX, value):
        raise ValidationError("Email formati noto'g'ri.")


def validate_phone_number(value):
    if not re.fullmatch(PHONE_REGEX, value):
        raise ValidationError(
            "Telefon raqam + va 9-15 ta raqamdan iborat bo'lishi kerak."
        )
