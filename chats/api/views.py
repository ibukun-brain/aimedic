import pusher
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import get_object_or_404
from django_q.tasks import async_task
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import generics, status

from aimedic.utils.settings import get_env_variable
from chats.api.serializers import (
    ChannelDetailSerializer,
    ChannelSerializer,
    UserAIChatSerializer,
    UserPractitionerChannelDetailSerializer,
    UserPractitionerChatSerializer,
    UserPractitionerCreateChatSerializer,
)
from chats.models import Channel, UserAIChat, UserPractitionerChannel
from chats.tasks import chat_ai_task, summarize_channel_title_task
from home.api import custom_permissions
from practitioner.api.serializers import PractitionerPatientSerializer
from practitioner.models import PractitionerPatient

pusher_client = pusher.Pusher(
    app_id=get_env_variable("PUSHER_APP_ID", "XXXX"),
    key=get_env_variable("PUSHER_KEY", "XXXX"),
    secret=get_env_variable("PUSHER_SECRET", "XXXX"),
    cluster=get_env_variable("PUSHER_CLUSTER", "XXXX"),
)


class ChannelListAPIView(generics.ListAPIView):
    serializer_class = ChannelSerializer
    queryset = Channel.objects.none()
    permission_classes = [custom_permissions.IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        qs = (
            Channel.objects.prefetch_related("useraichat")
            .select_related("user")
            .filter(user=user)
        )
        return qs

    @extend_schema(
        summary="Channel lists",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Success",
                examples=[
                    OpenApiExample(
                        "200 OK response",
                        value={
                            "pk": "67bd3bab-dfad-4362-9733-52c4d1b433fd",
                            "title": "Hi there, have been experiencing certain symptoms"
                        },
                    )
                ],
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response={
                    "detail": "Authentication credentials were not provided.",
                },
                description="Unauthorized",
                examples=[
                    OpenApiExample(
                        "401 UNAUTHORIZED Response",
                        value={
                            "detail": "Authentication credentials were not provided."
                        },
                    )
                ],
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        This endpoint returns a channels for AI chat, A channel consists
        of multiple chats to the AI
        """
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChannelDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Channel.objects.none()
    serializer_class = ChannelDetailSerializer

    def get_object(self):
        pk = self.kwargs["pk"]
        try:
            obj = (
                Channel.objects.prefetch_related("useraichat")
                .select_related("user")
                .get(pk=pk)
            )
        except Channel.DoesNotExist as e:
            raise Http404 from e
        return obj


class ChannelRenameAPIView(generics.UpdateAPIView):
    queryset = Channel.objects.select_related("user").all()
    serializer_class = ChannelSerializer

    def get_object(self):
        pk = self.kwargs["pk"]
        obj = Channel.objects.select_related("user").get(pk=pk)
        return obj

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class UserAIChatCreateAPIView(generics.CreateAPIView):
    pusher_event_name = "user_chat"
    serializer_class = UserAIChatSerializer
    queryset = UserAIChat.objects.select_related("user").all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        text = serializer.validated_data.get("text")
        ai_chat_id = serializer.validated_data.get("id")
        channel = Channel.objects.create(title=text, user=self.request.user)
        async_task(summarize_channel_title_task, channel.id, channel.title)
        async_task(chat_ai_task, text, ai_chat_id)
        # call celery or threading to save ai response
        serializer.save(user=self.request.user, channel=channel)


class UserPractitionerChatListAPIView(generics.ListAPIView):
    serializer_class = PractitionerPatientSerializer
    queryset = PractitionerPatient.objects.all()

    def get_queryset(self):
        qs = PractitionerPatient.objects.select_related("patient", "practitioner")
        request = self.request
        if request.user.is_practitioner:
            cache_obj = cache.get("patient_list")
            if cache_obj is None:
                qs = qs.filter(practitioner=request.user.practitioner)
                cache.set("patient_list", qs)
            return qs
        # if user is a patient
        cache_obj = cache.get("practitioner_list")
        if cache_obj is None:
            qs = qs.filter(patient=request.user)
            cache.set("patient_list", qs)
        return qs

    def get_serializer_class(self):
        if self.request.user.is_practitioner:
            return self.serializer_class
        return UserPractitionerChatSerializer


class UserPractitionerChannelDetailAPIView(generics.RetrieveAPIView):
    """Endpoint to view messages" between patient(user) and practitioner"""

    serializer_class = UserPractitionerChannelDetailSerializer

    def get_object(self):
        pk = self.kwargs["pk"]
        obj = UserPractitionerChannel.objects.prefetch_related("chats")
        # cache_obj = cache.get("user_practitioner_channel")
        # if cache_obj is None:
        obj = get_object_or_404(obj, pk=pk)
        # cache.set("user_practitioner_channel", obj)
        return obj
        # return cache_obj


class UserPractitionerChannelChatCreateAPIView(generics.CreateAPIView):
    """Endpoint to create/send messages or chat"""

    # serializer_class = UserChannelChatSerializer
    serializer_class = UserPractitionerCreateChatSerializer
    queryset = None
    pusher_event_name = "send_chat"

    # def get_serializer_class(self):
    #     if self.request.user.is_practitioner:
    #         return PractitionerChatSerializer
    #     return self.serializer_class

    def perform_create(self, serializer):
        chat_id = self.kwargs["chat_id"]
        user_practitioner_channel = UserPractitionerChannel.objects.prefetch_related(
            "chats"
        )
        user_practitioner_channel = get_object_or_404(
            user_practitioner_channel, pk=chat_id
        )
        if self.request.user.is_practitioner:
            serializer.save(
                channel=user_practitioner_channel,
                practitioner=self.request.user.practitioner,
            )
        else:
            serializer.save(
                channel=user_practitioner_channel, patient=self.request.user
            )
        # trigger client with django_q
        pusher_client.trigger(
            f"userpractitionerchannelchat_{chat_id}",
            "send_chat",
            {
                "text": serializer.validated_data.get("text"),
                "profile_picture": serializer.data.get("profile_picture"),
                "sender": serializer.data.get("sender"),
            },
        )
