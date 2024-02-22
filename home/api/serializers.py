import email
import threading

import pyotp
from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone

# from django_q.tasks import async_task
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import RefreshToken

from home.models import CustomUser
from home.tasks import send_email_task, send_user_otp_task

User = get_user_model()


class BaseOTPSerializer(serializers.Serializer):
    def generate_otp(self, interval=None, resend=False):
        totp = pyotp.TOTP(
            "base32secret3232",
            digits=4,
            interval=interval,
        )
        if resend:
            return self.generate_otp(interval=600)
        return totp

    def validate(self, attrs):
        request = self.context.get("request")
        email = request.session.get("email") or attrs.get("email")
        otp = attrs.get("otp")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist as e:
            raise exceptions.AuthenticationFailed("Authentication Failed") from e

        if not self.generate_otp(interval=attrs.get("interval")).verify(otp):
            raise serializers.ValidationError({"otp": "Invalid OTP"})
        attrs["user"] = user
        del request.session["email"]
        return super().validate(attrs)


class GenerateOTPSerializer(BaseOTPSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, attrs: dict):
        email = attrs.get("email").lower().strip()
        attrs["interval"] = 600  # interval to generate OTP
        request = self.context.get("request")
        user = authenticate(
            request=request,
            email=email,
            password=attrs.get("password"),
        )
        if user is None:
            raise exceptions.AuthenticationFailed("Invalid login details.")
        attrs["user_object"] = user
        request.session["email"] = email

        return attrs

    def create(self, validated_data: dict):
        user = validated_data.get("user_object")
        otp = self.generate_otp(interval=validated_data.get("interval")).now()
        subject = "OTP Verification"
        message = f"Hi there, your otp is {otp}\nexpires in 10 minutes"
        send_user_otp_task(user, subject, message, otp)
        # st_task(send_user_otp_task, user, subject, message)
        # thread = threading.Thread(
        #     target=send_user_otp_task, args=[user, subject, message, otp], daemon=True
        # )
        # thread.start()
        # i don't know if django_q will run on vercel but i will assume,
        # if it doesn't workreplace where u used django_q and proceed with
        # django_crontab
        return user


class VerifyOTPSerializer(BaseOTPSerializer):
    otp = serializers.CharField(max_length=4)

    def validate(self, attrs):
        attrs["interval"] = 600  # time counter
        return super().validate(attrs)

    def create(self, validated_data: dict):
        user = validated_data.get("user")
        refresh = RefreshToken.for_user(user)
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])
        return {
            "success": True,
            "message": "OTP verified successfully",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class ResendOTPSerializer(BaseOTPSerializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        email = validated_data.get("email")
        request.session["email"] = email
        otp = self.generate_otp(interval=600).now()
        subject = "OTP Verification"
        message = f"Hi there, your otp is {otp}\nexpires in 10 minutes"
        send_email_task(subject, message, email, otp)
        # thread_send_email = threading.Thread(
        #     target=send_email_task, args=[subject, message, email, otp], daemon=True
        # )
        # thread_send_otp = threading.Thread(
        #     target=send_user_otp_task, args=[subject, message, email, otp], daemon=True
        # )
        # thread_send_email.start()
        # thread_send_otp.start()
        # async_task(send_email_task, subject, message, email)
        # send_user_otp_task(subject, message, email)
        data = {
            "success": True,
            "message": "OTP Sent",
            "email": email,
        }
        return data


# @extend_schema_serializer(
#     examples=[
#         OpenApiExample(
#             'Success response',
#             value={
#                 'access': "string",
#                 'token': "string"
#             },
#             response_only=True,
#         )
#     ]
# )
# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     # otp = serializers.CharField(max_length=4)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.fields["otp"] = serializers.CharField(max_length=4)

#     @classmethod
#     def get_token(cls, user):
#         return cls.token_class.for_user(user)

#     def validate(self, attrs):
#         super().validate(attrs)

#     def validate_otp(self, data):
#         if not self.otp.verify(data):
#             raise serializers.ValidationError("Invalid OTP code")


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = [
            "first_name",
            "last_name",
            # "type",
            # "date_of_birth",
            "email",
            "gender",
            "password",
        ]


class CustomUserSerializer(UserSerializer):
    # image = serializers.SerializerMethodField("_image_url")

    # @extend_schema_field(OpenApiTypes.URI)
    # def _image_url(self, obj):
    #     request = self.context["request"]
    #     url = get_url(request, path_str=None, default=settings.STATIC_URL)
    #     if obj.profile_pic:
    #         return obj.profile_pic.url

    #     return f"{url}image/placeholder.jpg"

    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = (
            "id",
            "first_name",
            "last_name",
            "type",
            "gender",
            "profile_pic",
            "email",
            "age",
        )
        extra_kwargs = {
            "first_name": {
                "read_only": True,
            },
            "last_name": {
                "read_only": True,
            },
            "email": {
                "read_only": True,
            },
        }
