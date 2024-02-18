from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from home.api.views import PatientPractitionerListAPIView
from home.views import run_cronjob

urlpatterns = [
    path(
        "api/patients/",
        PatientPractitionerListAPIView.as_view(),
        name="patients-practitioner",
    ),
    path("api/cron/", run_cronjob, name="cronjob"),
    path(
        "api/appointments/", include("appointments.api.urls", namespace="appointments")
    ),
    path("api/chats/", include("chats.api.urls", namespace="chats")),
    path(
        "api/classification/",
        include("classification.api.urls", namespace="classification"),
    ),
    path(
        "api/notifications/", include("notification.api.urls", namespace="notification")
    ),
    path(
        "api/practitioners/", include("practitioner.api.urls", namespace="practitioner")
    ),
    path("api/auth/", include("home.api.urls", namespace="home")),
    path("api/auth/", include("djoser.urls")),
    # path("api/auth/", include("djoser.urls.jwt")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-docs",
    ),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    extrapatterns = [path("__debug__/", include("debug_toolbar.urls"))]
    urlpatterns += extrapatterns
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
