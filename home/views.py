from django.http import HttpResponse
from django.core.mail import send_mail


def run_cronjob(request):
    send_mail(
        "Cron job",
        "cron job ran",
        from_email="noreply@afrimed.com",
        recipient_list=[
            "ibukunolaifa@gmail.com",
            "ibukunolaifa1984@gmail.com"
        ]
    )
    print("running cronjob")
    return HttpResponse("Ok")
