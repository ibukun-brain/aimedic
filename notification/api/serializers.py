from notifications.models import Notification
from notifications.utils import id2slug
from rest_framework import serializers

from chats.api.serializers import UserImageSerializer
from home.models import CustomUser

# class GenericNotificationRelatedField(serializers.RelatedField):

#     def to_representation(self, value):
#         if isinstance(value, Foo):
#             serializer = FooSerializer(value)
#         if isinstance(value, Bar):
#             serializer = BarSerializer(value)

#         return serializer.data


class NotificationSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()
    sender = serializers.SerializerMethodField()
    # recipient = UserImageSerializer(read_only=True, many=False)
    natural_time = serializers.SerializerMethodField()
    # recipient = serializers.StringRelatedField
    # unread = serializers.BooleanField(read_only=True)
    # target = GenericNotificationRelatedField(read_only=True)

    class Meta:
        model = Notification
        # fields = "__all__"
        fields = [
            "slug",
            "timestamp",
            "natural_time",
            "sender",
            "unread",
            "verb",
            "description",
        ]

    def get_natural_time(self, obj) -> str:
        from django.contrib.humanize.templatetags.humanize import naturaltime

        return naturaltime(obj.timestamp)

    def get_sender(self, obj) -> dict:
        user = CustomUser.objects.get(id=obj.actor_object_id)
        return UserImageSerializer(user).data

    def get_slug(self, obj) -> int:
        return id2slug(obj.id)
