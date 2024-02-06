from django.urls import path

from home.api import views

app_name = "home"

urlpatterns = [
    path("otp/generate/", views.GenerateOTPAPIView.as_view(), name="generate-otp"),
    path("otp/verify/", views.VerifyOTPAPIView.as_view(), name="generate-otp"),
    path("otp/resend/", views.ResendOTPAPIView.as_view(), name="resend-otp"),
]
