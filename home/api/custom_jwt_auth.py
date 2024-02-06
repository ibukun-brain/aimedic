from django.contrib.auth.signals import user_logged_in
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    """
    The only difference between this CustomJWTAuthentication
    and JwTAuthentication is that this custom jwt authentication sends a
    user_logged_in signal which we can use to perform various actions
    when a user is authenticated
    """

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)
        user_logged_in.send(sender=user.__class__, request=request, user=user)
        return self.get_user(validated_token), validated_token
