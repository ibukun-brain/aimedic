DJOSER = {
    "USER_ID_FIELD": "pk",
    "LOGIN_FIELD": "email",
    # "USER_CREATE_PASSWORD_RETYPE": True,
    "SET_PASSWORD_RETYPE": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    # "SEND_ACTIVATION_EMAIL": True,
    # "SEND_CONFIRMATION_EMAIL": True,
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL": "password/reset/{uid}/{token}",
    "PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND": True,
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "SERIALIZERS": {
        # if user_create_password is True then user_create_password_retype serializer will be used
        # instead or user_create_serializer
        # "user_create_password_retype": "home.api.serializers.CustomUserCreatePasswordRetypeSerializer",
        "user_create": "home.api.serializers.CustomUserCreateSerializer",
        "user": "home.api.serializers.CustomUserSerializer",
        "current_user": "home.api.serializers.CustomUserSerializer",
        'token_create': 'djoser.serializers.TokenCreateSerializer',
    },
    "SOCIAL_AUTH_TOKEN_STRATEGY": "djoser.social.token.jwt.TokenStrategy",
    "SOCIAL_AUTH_ALLOWED_REDIRECT_URIS": [
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3000/home",
        "http://127.0.0.1:3000/login",
        "http://localhost:8000/accounts/profile/",
        "http://127.0.0.1:8000/accounts/profile/",
    ],
}
