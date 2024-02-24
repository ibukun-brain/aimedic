from django.urls import path

from classification.api import views

app_name = "classification"

urlpatterns = [
    path(
        "heart_disease/",
        views.HeartClassificationAPIView.as_view(),
        name="heart-classification",
    ),
    path(
        "image_detection/",
        views.ImageDetectionAPIView.as_view(),
        name="image-detection",
    ),
]
