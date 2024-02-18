from django.urls import path

from notification.api import views

app_name = "notification"

urlpatterns = [
    path("", views.AllNotificationListAPIView.as_view(), name="all"),
    path(
        "read_notification/<int:slug>/",
        views.ReadNotificationDetailAPIView.as_view(),
        name="all",
    ),
]
