import os

from django.core.wsgi import get_wsgi_application

# from aimedic.settings import base_settings

# if base_settings.DEBUG:
#     os.environ.setdefault(
#         "DJANGO_SETTINGS_MODULE", "aimedic.settings.development_settings"
#     )

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aimedic.settings.production_settings")

application = get_wsgi_application()

app = application
