from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from chats.api.serializers import UserPractitionerChatSerializer
from home.api.serializers import (
    GenerateOTPSerializer,
    ResendOTPSerializer,
    VerifyOTPSerializer,
)
from practitioner.models import PractitionerPatient


class AllowAnyPermissionMixins:
    permission_classes = [permissions.AllowAny]


class GenerateOTPAPIView(AllowAnyPermissionMixins, generics.GenericAPIView):
    """
    If the request is successful, an otp is sent to the user's email
    Verify the otp at the /verify endpoint to get the access token
    to be used for authenticating the user
    """

    serializer_class = GenerateOTPSerializer

    @extend_schema(
        summary="Login endpoint for both patients and doctors/practitioners",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response={
                    "success": True,
                    "user": "user@email.com",
                    "message": "OTP sent",
                },
                description="Success",
                examples=[
                    OpenApiExample(
                        "200 OK response",
                        value={
                            "success": True,
                            "user": "user@email.com",
                            "message": "OTP sent",
                        },
                    )
                ],
            ),
        },
    )
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "success": True,
                "user": user.email,
                "message": "OTP sent",
            },
            status=status.HTTP_200_OK,
        )


class VerifyOTPAPIView(AllowAnyPermissionMixins, generics.GenericAPIView):
    """Verify OTP"""

    serializer_class = VerifyOTPSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        methods=["POST"],
        summary="Verify OTP sent to the user email",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response={
                    "success": True,
                    "message": "OTP Verified",
                    "refresh": "string",
                    "access": "string",
                },
                description="Success",
                examples=[
                    OpenApiExample(
                        "200 OK response",
                        value={
                            "success": True,
                            "message": "OTP Verified",
                            "refresh": "string",
                            "access": "string",
                        },
                    )
                ],
            ),
        },
    )
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login_info = serializer.save()
        return Response(login_info, status=200)


class ResendOTPAPIView(AllowAnyPermissionMixins, generics.GenericAPIView):
    """Resend OTP"""

    serializer_class = ResendOTPSerializer

    @extend_schema(
        methods=["POST"],
        summary="Resend OTP",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response={
                    "success": True,
                    "message": "OTP Sent",
                    "email": "admin@example.com",
                },
                description="Success",
                examples=[
                    OpenApiExample(
                        "200 OK response",
                        value={
                            "success": True,
                            "message": "OTP Sent",
                            "email": "admin@example.com",
                        },
                    )
                ],
            ),
        },
    )
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.save()
        return Response(response, status=200)


class PatientPractitionerListAPIView(generics.ListAPIView):
    serializer_class = UserPractitionerChatSerializer
    queryset = PractitionerPatient.objects.all()

    @extend_schema(summary="patient's practitioner/doctors listing")
    def get(self, request, *args, **kwargs):
        """
        The endpoint returns the patient's doctors/practitioners, basically
        the doctors/practitioners are those who has accepted an appointment
        request from the doctors
        """
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        patient = self.request.user
        qs = PractitionerPatient.objects.filter(patient=patient)
        return qs
