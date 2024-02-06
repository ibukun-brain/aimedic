from django.urls import path

from chats.api import views

app_name = "chats"

urlpatterns = [
    path(
        "channels/chatbot/", views.ChannelListAPIView.as_view(), name="channels-chatbot"
    ),
    path(
        "channels/chatbot/<uuid:pk>/",
        views.ChannelDetailAPIView.as_view(),
        name="channels-chatbot-detail",
    ),
    path(
        "channels/chatbot/<uuid:pk>/rename/",
        views.ChannelRenameAPIView.as_view(),
        name="channels-chatbot-rename",
    ),
    path(
        "channels/chatbot/",
        views.UserAIChatCreateAPIView.as_view(),
        name="channels-chatbot-chat",
    ),
    path(
        "channels/chats/",
        views.UserPractitionerChatListAPIView.as_view(),
        name="channels-chats",
    ),
    path(
        "channels/chats/<uuid:pk>/",
        views.UserPractitionerChannelDetailAPIView.as_view(),
        name="channels-chats-detail",
    ),
    path(
        "channels/chats/<uuid:chat_id>/send/",
        views.UserPractitionerChannelChatCreateAPIView.as_view(),
        name="channels-chat-send",
    ),
]
