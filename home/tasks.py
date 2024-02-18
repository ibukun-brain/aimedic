from django.core.mail import send_mail

# from templated_mail.mail import BaseEmailMessage
from aimedic.settings.local.email_settings import DEFAULT_FROM_EMAIL


def send_user_otp_task(user, subject, message):
    # BaseEmailMessage(
    #     context={"otp": otp},
    #     template_name='email/generate_otp.html').send(to=[user.email])

    user.email_user(
        subject=subject,
        message=message,
        from_email=DEFAULT_FROM_EMAIL,
    )


def send_email_task(subject, message, email, otp=None):
    send_mail(
        subject=subject,
        message=message,
        recipient_list=[email],
        from_email=DEFAULT_FROM_EMAIL,
    )
