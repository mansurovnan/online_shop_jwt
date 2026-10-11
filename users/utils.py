
from django.conf import settings
from django.core.mail import send_mail


def send_welcome_email(user):
    subject = "Welcome to Online Shop"

    message = (
        f"Hello, {user.username}!\n\n"
        "Welcome to our Online Shop platform.\n"
        "Thank you for joining us!"
    )

    return send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
