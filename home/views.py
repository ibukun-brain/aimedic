from django.core.mail import send_mail
from django.http import HttpResponse

from aimedic.settings.local.email_settings import DEFAULT_FROM_EMAIL


def run_cronjob(request):
    send_mail(
        subject="Cron job",
        message="cron job ran",
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[
            "ibukunolaifa@gmail.com",
            "ibukunolaifa1984@gmail.com"
        ]
    )
    print("running cronjob")
    return HttpResponse("Ok")
