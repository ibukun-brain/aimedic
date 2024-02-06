from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from chats.models import (  # PractitionerChannelChat,; UserChannelChat,
    Channel,
    UserAIChat,
    UserPractitionerChannel,
    UserPractitionerChannelChat,
)
from home.models import CustomUser
from practitioner.models import Practitioner, PractitionerPatient


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = [
            "pk",
            "title",
        ]

    def create(self, validated_data):
        return Channel.objects.create(**validated_data)


class UserAIChatSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=500)

    class Meta:
        model = UserAIChat
        fields = [
            "text",
            "response",
            "image",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "response": {
                "read_only": True,
            },
        }

    def create(self, validated_data):
        return UserAIChat.objects.create(**validated_data)


class ChannelDetailSerializer(serializers.ModelSerializer):
    useraichat = UserAIChatSerializer(many=True)

    class Meta:
        model = Channel
        fields = [
            "pk",
            "title",
            "useraichat",
        ]


# class UserChannelChatSerializer(serializers.ModelSerializer):
#     profile_picture = serializers.SerializerMethodField()
#     name = serializers.SerializerMethodField()
#     is_me = serializers.SerializerMethodField()

#     class Meta:
#         model = UserChannelChat
#         fields = [
#             "text",
#             "name",
#             "profile_picture",
#             "is_me",
#             "created_at",
#         ]

#     def get_profile_picture(self, obj) -> str:
#         return obj.user.image_url

#     def get_name(self, obj):
#         return obj.user.get_full_name()

#     def get_is_me(self, obj):
#         request = self.context["request"]
#         return request.user == obj.user


# class PractitionerChatSerializer(serializers.ModelSerializer):
#     profile_picture = serializers.SerializerMethodField()
#     name = serializers.SerializerMethodField()
#     is_me = serializers.SerializerMethodField()

#     class Meta:
#         model = PractitionerChannelChat
#         fields = [
#             "text",
#             "name",
#             "profile_picture",
#             "is_me",
#             "created_at",
#         ]

#     def get_is_me(self, obj):
#         request = self.context["request"]
#         return request.user.practitioner == obj.practitioner

#     def get_profile_picture(self, obj) -> str:
#         return obj.practitioner.user.image_url

#     def get_name(self, obj) -> str:
#         return obj.practitioner.user.get_full_name()


# class UserPractitionerChannelDetailSerializer(serializers.ModelSerializer):
#     patient = UserChannelChatSerializer(many=True)
#     practitioner = PractitionerChatSerializer(many=True)

#     class Meta:
#         model = UserPractitionerChannel
#         fields = [
#             "id",
#             "patient",
#             "practitioner",
#         ]


class UserPractitionerCreateChatSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    sender = serializers.SerializerMethodField()

    class Meta:
        model = UserPractitionerChannelChat
        fields = [
            "text",
            "sender",
            "profile_picture",
        ]

    def get_profile_picture(self, obj) -> str:
        request = self.context["request"]
        return request.user.image_url

    def get_sender(self, obj) -> bool:
        request = self.context["request"]
        if request.user.is_practitioner:
            return request.user.practitioner == obj.practitioner
        return request.user == obj.patient

    def create(self, validated_data):
        return UserPractitionerChannelChat.objects.create(**validated_data)


class UserPractitionerChannelChatSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    sender = serializers.SerializerMethodField()

    class Meta:
        model = UserPractitionerChannelChat
        fields = [
            "text",
            "name",
            "profile_picture",
            "sender",
            "created_at",
        ]

    def get_sender(self, obj) -> bool:
        request = self.context["request"]
        if request.user.is_practitioner:
            return request.user.practitioner == obj.practitioner
        return request.user == obj.patient

    def get_profile_picture(self, obj) -> str:
        if obj.practitioner:
            return obj.practitioner.user.image_url
        return obj.patient.image_url

    def get_name(self, obj) -> str:
        if obj.practitioner:
            return obj.practitioner.user.get_full_name()
        return obj.patient.get_full_name()


class UserPractitionerChannelDetailSerializer(serializers.ModelSerializer):
    chats = UserPractitionerChannelChatSerializer(many=True)

    class Meta:
        model = UserPractitionerChannel
        fields = [
            "id",
            "chats",
        ]


class UserImageSerializer(serializers.ModelSerializer):
    """Serializer for showing chat lists it contains user name and images"""

    name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "name",
            "image_url",
        ]

    def get_name(self, obj) -> str:
        return obj.get_full_name()


class PractitionerChatListSerializer(serializers.ModelSerializer):
    user = UserImageSerializer(many=False)

    class Meta:
        model = Practitioner
        fields = ["user"]


class UserPractitionerChatSerializer(serializers.ModelSerializer):
    """Users/Patients chats list"""

    chat_id = serializers.SerializerMethodField()  # chat or channel id
    practitioner = PractitionerChatListSerializer(many=False)

    class Meta:
        model = PractitionerPatient
        fields = [
            "chat_id",
            "practitioner",
        ]

    @extend_schema_field(OpenApiTypes.UUID)
    def get_chat_id(self, obj):
        return obj.userpractitionerchannel.id

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["details"] = data.pop("practitioner")["user"]
        return data
