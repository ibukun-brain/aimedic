from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from notifications import settings as notification_settings
from notifications.models import Notification
from notifications.utils import slug2id
from rest_framework import generics, status

from notification.api.serializers import NotificationSerializer


class AllNotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def get_queryset(self):
        if notification_settings.get_config()["SOFT_DELETE"]:
            qs = self.request.user.notifications.active()
        else:
            qs = self.request.user.notifications.all()
        return qs

    @extend_schema(
        summary="All notifications",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response={
                    "slug": 123123,
                    "timestamp": "2024-02-18T10:42:31.385Z",
                    "natural_time": "2s ago",
                    "sender": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "name": "Ayanokoji Kenjaku",
                        "image_url": "string",
                    },
                    "unread": True,
                    "verb": "You have an appointment request",
                    "description": "Ayanokoji Kenjaku sent an appointment" +
                    "request, accept or decline.",
                },
                examples=[
                    OpenApiExample(
                        name="unread notification",
                        value={
                            "slug": 123123,
                            "timestamp": "2024-02-18T10:42:31.385Z",
                            "natural_time": "2s ago",
                            "sender": {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "name": "Ayanokoji Kenjaku",
                                "image_url": "string",
                            },
                            "unread": True,
                            "verb":
                            "You have an appointment request",
                            "description": "Ayanokoji Kenjaku sent an appointment" +
                            "request, accept or decline.",
                        },
                    ),
                    OpenApiExample(
                        name="read notification",
                        value={
                            "slug": 123123,
                            "timestamp": "2024-02-18T10:42:31.385Z",
                            "natural_time": "2s ago",
                            "sender": {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "name": "Ayanokoji Kenjaku",
                                "image_url": "string",
                            },
                            "unread": False,
                            "verb":
                            "You have an appointment request",
                            "description": "Ayanokoji Kenjaku sent an appointment" +
                            "request, accept or decline.",
                        },
                    ),
                ],
            )
        },
    )
    def get(self, request, *args, **kwargs):
        """All notifications including read and unread notification"""
        return self.list(request, *args, **kwargs)


class ReadNotificationDetailAPIView(generics.RetrieveAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def get_object(self):
        slug = self.kwargs["slug"]
        # notification_slug = id2slug(id)
        notification_id = slug2id(slug)

        notification = get_object_or_404(
            Notification, recipient=self.request.user, id=notification_id
        )
        notification.mark_as_read()

        return notification

    @extend_schema(
        summary="read notification",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response={
                    "slug": 123123,
                    "timestamp": "2024-02-18T10:42:31.385Z",
                    "natural_time": "2s ago",
                    "sender": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "name": "Ayanokoji Kenjaku",
                        "image_url": "string",
                    },
                    "unread": False,
                    "verb": "You have an appointment request",
                    "description":
                    "Ayanokoji Kenjaku sent an appointment request, accept or decline.",
                },
                examples=[
                    OpenApiExample(
                        name="read notification",
                        value={
                            "slug": 123123,
                            "timestamp": "2024-02-18T10:42:31.385Z",
                            "natural_time": "2s ago",
                            "sender": {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "name": "Ayanokoji Kenjaku",
                                "image_url": "string",
                            },
                            "unread": False,
                            "verb": "You have an appointment request",
                            "description": "Ayanokoji Kenjaku sent an " +
                            "appointment request, accept or decline.",
                        },
                    )
                ],
            )
        },
    )
    def get(self, request, *args, **kwargs):
        """This endpoint mark a notification instance as read"""
        return self.retrieve(request, *args, **kwargs)
