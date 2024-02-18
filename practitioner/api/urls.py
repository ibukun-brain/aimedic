from django.urls import path

from practitioner.api import views

app_name = "practitioner"

urlpatterns = [
    path("", views.PractitionerListAPIView.as_view(), name="practitioner"),
    path(
        "signup/",
        views.PractitionerSignupCreateAPIView.as_view(),
        name="practitioner-signup",
    ),
    path(
        "overview/",
        views.PractitionerOverviewAPIView.as_view(),
        name="practitioner-overview",
    ),
    path(
        "patients/",
        views.PractitionerPatientsListAPIView.as_view(),
        name="practitioner-patients",
    ),
]
