from django.http import HttpResponse


def run_cronjob(request):
    print("running cronjob")
    return HttpResponse("Ok")
