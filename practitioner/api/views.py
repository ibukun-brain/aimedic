from rest_framework import generics, permissions, serializers

from home.api import custom_permissions
from practitioner.api.serializers import (
    PractitionerOverviewSerializer,
    PractitionerPatientSerializer,
    PractitionerSerializer,
)
from practitioner.models import Practitioner, PractitionerPatient


class PractitionerListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PractitionerSerializer
    queryset = Practitioner.objects.none()

    def get_queryset(self):
        qs = Practitioner.objects.select_related('user').all()
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PractitionerOverviewAPIView(generics.RetrieveAPIView):
    serializer_class = PractitionerOverviewSerializer
    permission_classes = [
        custom_permissions.IsOwnerOrReadOnly,
        permissions.IsAuthenticated
    ]
    queryset = Practitioner.objects.all()

    def get_object(self):
        user = self.request.user
        try:
            return Practitioner.objects.get(user=user)
        except Practitioner.DoesNotExist:
            raise serializers.ValidationError(
                {"error": "Practitioner does not exist"}
            )


class PractitionerPatientsListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PractitionerPatientSerializer
    queryset = PractitionerPatient.objects.all()

    def get_queryset(self):
        practitioner = self.request.user.practitioner
        qs = PractitionerPatient.objects.filter(practitioner=practitioner)
        return qs
