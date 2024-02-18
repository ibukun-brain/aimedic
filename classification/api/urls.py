from django.urls import path

from classification.api import views

app_name = "classification"

urlpatterns = [
    path(
        "heart_disease/",
        views.HeartClassificationAPIView.as_view(),
        name="heart-classification",
    ),
]
