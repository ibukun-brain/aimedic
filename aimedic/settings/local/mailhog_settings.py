EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "localhost"

EMAIL_PORT = 1025

EMAIL_HOST_USER = "nobody@gmail.com"
# DEFAULT_FROM_EMAIL = "noreply@aimedic.com"

DEFAULT_FROM_EMAIL = f"aimedic <{EMAIL_HOST_USER}>"
