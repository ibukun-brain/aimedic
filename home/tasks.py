import os

# from templated_mail.mail import BaseEmailMessage
from django.conf import settings
from django.core.mail import send_mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))


def send_user_otp_task(user, subject, message, otp):
    # BaseEmailMessage(
    #     context={"otp": otp},
    #     template_name='email/generate_otp.html').send(to=[user.email])

    # user.email_user(
    #     subject=subject,
    #     message=message,
    #     from_email=settings.DEFAULT_FROM_EMAIL,
    # )
    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=user.email,
        subject=subject,
        html_content=message
    )
    try:
        sg.send(message)
    except Exception as e:
        print(e)


def send_email_task(subject, message, email, otp=None):
    # send_mail(
    #     subject=subject,
    #     message=message,
    #     recipient_list=[email],
    #     from_email=settings.DEFAULT_FROM_EMAIL,
    # )
    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=email,
        subject=subject,
        html_content=message
    )
    try:
        sg.send(message)
    except Exception as e:
        print(e)
