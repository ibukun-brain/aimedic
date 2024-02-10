from datetime import datetime

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions

from aimedic.utils.choices import AppointmentStatus
from appointments.api import custom_permissions
from appointments.api.serializers import (
    PatientAppointmentSerializer,
    PatientCreateAppointmentSerializer,
    PractitionerAcceptOrDeclineAppointmentSerializer,
    PractitionerAppointmentSerializer,
)
from appointments.models import Appointment
from practitioner.models import Practitioner


class PatientPendingAppointmentListAPIView(generics.ListAPIView):
    """
    Endpoint for patient pending appointment that has not been accepted
    by the doctor/practitioner
    """

    serializer_class = PatientAppointmentSerializer

    @extend_schema(summary="patient's pending appointment")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        qs = Appointment.objects.select_related("patient", "practitioner",).filter(
            patient=self.request.user, status=AppointmentStatus.Pending, completed=False
        )
        return qs


class PractitionerAppointmentRequestListAPIView(generics.ListAPIView):
    """
    Endpoint for practitioner to see appointment request
    """

    serializer_class = PractitionerAppointmentSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        custom_permissions.IsPractitionerOrReadOnly,
    ]
    queryset = Appointment.objects.all()

    @extend_schema(summary="practitioner appointment request")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        qs = Appointment.objects.select_related("patient", "practitioner",).filter(
            practitioner=self.request.user.practitioner,
            status=AppointmentStatus.Pending,
            completed=False,
        )
        return qs


class PatientAppointmentListAPIView(generics.ListAPIView):
    serializer_class = PatientAppointmentSerializer
    queryset = Appointment.objects.all()

    @extend_schema(summary="patient's active appointments")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        qs = Appointment.objects.select_related("patient", "practitioner",).filter(
            patient=self.request.user, status=AppointmentStatus.Active, completed=False
        )
        return qs


class PatientAppointmentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientAppointmentSerializer
    queryset = Appointment.objects.all()

    def get_object(self):
        appointment_id = self.kwargs["appointment_id"]
        obj = Appointment.objects.select_related("patient", "practitioner")
        obj = get_object_or_404(
            obj,
            id=appointment_id,
            patient=self.request.user,
            status=AppointmentStatus.Active,
        )
        return obj

    @extend_schema(summary="patient's active appointments detail")
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(summary="update patient's appointment")
    def put(self, request, *args, **kwargs):
        """Only pending appointments can be updated"""
        return self.update(request, *args, **kwargs)

    @extend_schema(summary="update patient's appointment")
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(summary="delete patient's appointment")
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_queryset(self):
        qs = Appointment.objects.select_related("patient", "practitioner",).filter(
            patient=self.request.user, status=AppointmentStatus.Active, completed=False
        )
        return qs


class PatientAppointmentCreateAPIView(generics.CreateAPIView):
    serializer_class = PatientCreateAppointmentSerializer
    queryset = Appointment.objects.all()

    @extend_schema(summary="create appointment with practitioner")
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        practitioner_id = self.kwargs["practitioner_id"]
        practitioner = get_object_or_404(Practitioner, id=practitioner_id)
        serializer.save(patient=self.request.user, practitioner=practitioner)


class PractitionerAppointmentListAPIView(generics.ListAPIView):

    serializer_class = PractitionerAppointmentSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        custom_permissions.IsPractitionerOrReadOnly,
    ]
    queryset = Appointment.objects.all()

    @extend_schema(summary="practitioner's appointments")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        qs = Appointment.objects.select_related("patient", "practitioner",).filter(
            practitioner=self.request.user.practitioner, status=AppointmentStatus.Active
        )
        return qs


class PractitionerAppointmentCreateAPIView(generics.CreateAPIView):
    serializer_class = PractitionerAcceptOrDeclineAppointmentSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        custom_permissions.IsPractitionerOrReadOnly,
    ]

    @extend_schema(summary="accept/decline appointments sent to practitioner")
    def post(self, request, *args, **kwargs):
        """Endpoint to acccept appointment sent to the practitioner"""
        return self.create(request, *args, **kwargs)

    def get_object(self):
        appointment_id = self.kwargs["appointment_id"]
        obj = Appointment.objects.select_related("patient", "practitioner")
        obj = get_object_or_404(
            obj, id=appointment_id, status=AppointmentStatus.Pending
        )
        return obj

    def perform_create(self, serializer):
        serializer.save(
            appointment_id=self.get_object(),
            practitioner=self.request.user.practitioner,
            patient=self.get_object().patient,
        )


class PractitionerTodayAppointmentListAPIView(generics.ListAPIView):
    serializer_class = PractitionerAppointmentSerializer
    queryset = Appointment.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        custom_permissions.IsPractitionerOrReadOnly,
    ]

    @extend_schema(summary="practitioner appointment for the day")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        qs = Appointment.objects.select_related("patient", "practitioner").filter(
            practitioner=self.request.user.practitioner,
            date_booked=datetime.now().date(),
            status=AppointmentStatus.Active,
        )
        return qs
