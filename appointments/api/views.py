from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions

from appointments.api import custom_permissions
from appointments.api.serializers import (
    PatientAppointmentSerializer,
    PatientCreateAppointmentSerializer,
    PractitionerAcceptAppointmentSerializer,
    PractitionerAppointmentSerializer,
)
from appointments.models import Appointment
from practitioner.models import Practitioner


class PatientAppointmentListAPIView(generics.ListAPIView):
    serializer_class = PatientAppointmentSerializer
    queryset = Appointment.objects.all()

    def get_queryset(self):
        qs = Appointment.objects.select_related(
            "patient",
            "practitioner",
        ).filter(patient=self.request.user, active=True)
        return qs


class PatientAppointmentCreateAPIView(generics.CreateAPIView):
    """Endpoint to send appointment to practitioner"""

    serializer_class = PatientCreateAppointmentSerializer
    queryset = None

    def perform_create(self, serializer):
        practitioner_id = self.kwargs["practitioner_id"]
        practitioner = get_object_or_404(Practitioner, id=practitioner_id)
        serializer.save(patient=self.request.user, practitioner=practitioner)


class PractitionerAppointmentListAPIView(generics.ListAPIView):
    """Endpoint for practitioner appointments"""

    serializer_class = PractitionerAppointmentSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        custom_permissions.IsPractitionerOrReadOnly,
    ]
    queryset = Appointment.objects.all()

    def get_queryset(self):
        qs = Appointment.objects.select_related(
            "patient",
            "practitioner",
        ).filter(practitioner=self.request.user.practitioner, active=True)
        return qs


class PractitionerAcceptAppointmentDetailAPIView(generics.RetrieveAPIView):
    """Endpoint to view appointment detail sent to the practitioner"""

    serializer_class = PractitionerAppointmentSerializer

    def get_object(self):
        appointment_id = self.kwargs["appointment_id"]
        obj = Appointment.objects.select_related("patient", "practitioner").get(
            id=appointment_id,
            active=True,
        )
        return obj


class PractitionerAcceptAppointmentUpdateAPIView(generics.UpdateAPIView):
    """Endpoint to acccept appointment sent to the practitioner"""

    serializer_class = PractitionerAcceptAppointmentSerializer

    def get_object(self):
        appointment_id = self.kwargs["appointment_id"]
        obj = Appointment.objects.select_related("patient", "practitioner").get(
            id=appointment_id,
            active=True,
        )
        return obj

    def perform_update(self, serializer):
        serializer.save(patient=self.get_object().patient)


class PractitionerTodayAppointmentListAPIView(generics.ListAPIView):
    serializer_class = PractitionerAppointmentSerializer
    queryset = Appointment.objects.all()

    def get_queryset(self):
        qs = Appointment.objects.select_related("patient", "practitioner").filter(
            practitioner=self.request.user.practitioner,
            date=datetime.now().date(),
            active=True,
        )
        return qs
