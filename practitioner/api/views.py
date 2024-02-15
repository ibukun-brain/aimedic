from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, serializers

from home.api import custom_permissions
from practitioner.api.serializers import (
    PractitionerCreateSerializer,
    PractitionerOverviewSerializer,
    PractitionerPatientSerializer,
    PractitionerSerializer,
)
from practitioner.models import Practitioner, PractitionerPatient


class PractitionerSignupCreateAPIView(generics.CreateAPIView):
    serializer_class = PractitionerCreateSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="signup as a doctor/practitioner",
        parameters=[
            # PractitionerCreateSerializer,
        ],
    )
    def post(self, request, *args, **kwargs):
        """Use this endpoint to signup as a doctor/practitioner"""
        return self.create(request, *args, **kwargs)


class PractitionerListAPIView(generics.ListAPIView):
    serializer_class = PractitionerSerializer
    queryset = Practitioner.objects.none()

    @extend_schema(summary="all doctors/practitioners listing")
    def get(self, request, *args, **kwargs):
        """This endpoint returns all doctors/practitioners listing"""
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        qs = Practitioner.objects.select_related("user").all()
        return qs


class PractitionerOverviewAPIView(generics.RetrieveAPIView):
    serializer_class = PractitionerOverviewSerializer
    permission_classes = [
        custom_permissions.IsOwnerOrReadOnly,
        permissions.IsAuthenticated,
    ]
    queryset = Practitioner.objects.all()

    def get_object(self):
        user = self.request.user
        try:
            return Practitioner.objects.get(user=user)
        except Practitioner.DoesNotExist as e:
            raise serializers.ValidationError(
                {"error": "Practitioner does not exist"}
            ) from e


class PractitionerPatientsListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PractitionerPatientSerializer
    queryset = PractitionerPatient.objects.all()

    def get_queryset(self):
        practitioner = self.request.user.practitioner
        qs = PractitionerPatient.objects.filter(practitioner=practitioner)
        return qs
