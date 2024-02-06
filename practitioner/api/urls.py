from django.urls import path
from practitioner.api import views

app_name = "practitioner"

urlpatterns = [
    path(
        "",
        views.PractitionerListCreateAPIView.as_view(),
        name="practitioner"
    ),
    path(
        "overview/",
        views.PractitionerOverviewAPIView.as_view(),
        name="practitioner-overview"
    ),
    path(
        "patients/",
        views.PractitionerPatientsListCreateAPIView.as_view(),
        name="practitioner-patients"
    )
]
