import dj_database_url

from aimedic.settings.local.email_settings import *
from aimedic.settings.packages.cloudinary_settings import *

from .base_settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable("SECRET_KEY", "XXXX")

ALLOWED_HOSTS.append("*")

INSTALLED_APPS.insert(5, "whitenoise.runserver_nostatic")
INSTALLED_APPS += [
    "cloudinary_storage",
    "cloudinary",
]

MIDDLEWARE.insert(2, "whitenoise.middleware.WhiteNoiseMiddleware")

DATABASES["default"] = dj_database_url.parse(
    get_env_variable(
        "PROD_DATABASE_URL", f"sqlite:////{BASE_DIR.joinpath(BASE_DIR.name)}.sqlite3"
    ),
    conn_max_age=600,
    conn_health_checks=True,
)

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"


# DATABASES["default"]["NAME"] = get_env_variable("DATABASE_NAME", "porfolio")
# DATABASES["default"]["ENGINE"] = "django.db.backends.postgresql"
# DATABASES["default"]["POOL_OPTIONS"] = {
#     "POOL_SIZE": 20,
#     "MAX_OVERFLOW": 30,
#     "RECYCLE": 24 * 60 * 60,
# }

SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 31536000
SECURE_REDIRECT_EXEMPT = []
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# SOCIAL_AUTH_JSONFIELD_ENABLED = True

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}
