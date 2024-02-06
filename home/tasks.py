from django.core.mail import send_mail


def send_user_otp_task(user, subject, message):
    user.email_user(
        subject=subject,
        message=message,
        from_email="noreply@aimedic.com",
    )


def send_email_task(subject, message, email):
    send_mail(
        subject=subject,
        message=message,
        recipient_list=[email],
        from_email="noreply@aimedic.com",
    )
