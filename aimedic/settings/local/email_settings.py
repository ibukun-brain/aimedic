from aimedic.utils.env_variable import get_env_variable

# Sending email configuration
EMAIL_HOST_USER = "apikey" or get_env_variable("EMAIL_HOST_USER", "XXX")

EMAIL_HOST_PASSWORD = (
    "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"
    or get_env_variable("EMAIL_HOST_PASSWORD", "XXX")
)

EMAIL_PORT = get_env_variable("EMAIL_PORT", "XXX")

EMAIL_HOST = "smtp.sendgrid.net" or get_env_variable("EMAIL_HOST", "XXX")

EMAIL_USE_SSL = True

# EMAIL_USE_TLS = True

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

SERVER_EMAIL = EMAIL_HOST_USER

DEFAULT_FROM_EMAIL = "ibukunolaifa1984@gmail.com" or EMAIL_HOST_USER

ADMINS = [(get_env_variable("ADMIN1", "XXX"), (get_env_variable("ADMIN2", "XXX")))]
