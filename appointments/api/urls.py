from django.urls import path

from appointments.api import views

app_name = "appointments"

urlpatterns = [
    path(
        "patients/",
        views.PatientAppointmentListAPIView.as_view(),
        name="appointment-patients",
    ),
    path(
        "patients/<uuid:appointment_id>/",
        views.PatientAppointmentDetailAPIView.as_view(),
        name="appointment-patients-detail",
    ),
    path(
        "patients/pending/",
        views.PatientPendingAppointmentListAPIView.as_view(),
        name="appointment-patients-pending",
    ),
    path(
        "practitioners/request/",
        views.PractitionerAppointmentRequestListAPIView.as_view(),
        name="appointment-requests",
    ),
    path(
        "practitioners/<uuid:practitioner_id>/",
        views.PatientAppointmentCreateAPIView.as_view(),
        name="appointment-patients-create",
    ),
    path(
        "practitioners/<uuid:appointment_id>/accept/",
        views.PractitionerAppointmentCreateAPIView.as_view(),
        name="appointment-accept-patients",
    ),
    path(
        "practitioners/",
        views.PractitionerAppointmentListAPIView.as_view(),
        name="appointment-practitioners",
    ),
    path(
        "practitioners/today/",
        views.PractitionerTodayAppointmentListAPIView.as_view(),
        name="appointment-practitioners-today",
    ),
]
