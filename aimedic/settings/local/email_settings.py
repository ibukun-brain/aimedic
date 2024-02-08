from aimedic.utils.env_variable import get_env_variable

# Sending email configuration
EMAIL_HOST_USER = get_env_variable("EMAIL_HOST_USER", "XXX")

EMAIL_HOST_PASSWORD = get_env_variable("EMAIL_HOST_PASSWORD", "XXX")

EMAIL_PORT = 587 or get_env_variable("EMAIL_PORT", "XXX")

EMAIL_HOST = get_env_variable("EMAIL_HOST", "XXX")

# EMAIL_USE_SSL = True

EMAIL_USE_TLS = True

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

SERVER_EMAIL = EMAIL_HOST_USER

DEFAULT_FROM_EMAIL = "noreply@afrimed.com" or EMAIL_HOST_USER

ADMINS = [(get_env_variable("ADMIN1", "XXX"), (get_env_variable("ADMIN2", "XXX")))]
