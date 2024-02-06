from aimedic.utils.env_variable import get_env_variable

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = get_env_variable(
    "SOCIAL_AUTH_GOOGLE_OAUTH2_KEY", "XXX-XXX"
)
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = get_env_variable(
    "SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET", "XXX-XXX"
)
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ["first_name", "last_name"]

SOCIAL_AUTH_USER_MODEL = "home.CustomUser"

SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
