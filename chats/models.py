import auto_prefetch
from django.core.cache import cache
from django.db import models
from django.forms import ValidationError
from django.template.defaultfilters import truncatechars
from django_lifecycle import (
    AFTER_DELETE,
    AFTER_SAVE,
    AFTER_UPDATE,
    LifecycleModelMixin,
    hook,
)
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from aimedic.utils.media import MediaHelper
from aimedic.utils.models import TimeBasedModel


class Channel(TimeBasedModel):
    title = models.CharField(max_length=130)
    user = auto_prefetch.ForeignKey(
        "home.CustomUser",
        on_delete=models.CASCADE,
    )

    @property
    @extend_schema_field(OpenApiTypes.STR)
    def trunc_title(self):
        return truncatechars(self.title, 50)

    def __str__(self):
        return self.trunc_title

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        indexes = [
            models.Index(fields=["-created_at", "-updated_at"])
        ]


class UserAIChat(TimeBasedModel):
    channel = auto_prefetch.ForeignKey(
        "chats.Channel",
        on_delete=models.CASCADE,
        related_name="useraichat"
    )
    image = models.ImageField(blank=True, upload_to=MediaHelper.get_image_upload_path)
    text = models.TextField()
    response = models.TextField(blank=True)
    user = auto_prefetch.ForeignKey("home.CustomUser", on_delete=models.CASCADE)

    @property
    @extend_schema_field(OpenApiTypes.STR)
    def trunc_text(self):
        return truncatechars(self.text, 50)

    def __str__(self):
        return self.trunc_text

    class Meta:
        ordering = ["created_at", "updated_at"]
        indexes = [
            models.Index(fields=["-created_at", "-updated_at"]),
        ]

    def clean(self):
        if self.channel.user != self.user:
            raise ValidationError("This channel does not belong this user")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class UserPractitionerChannel(TimeBasedModel):
    """private channel between user and practitioner"""
    chat = auto_prefetch.OneToOneField(
        "practitioner.PractitionerPatient",
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Practitioner and Patient"
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"])
        ]


class UserPractitionerChannelChat(LifecycleModelMixin, TimeBasedModel):
    channel = auto_prefetch.ForeignKey(
        "chats.UserPractitionerChannel",
        on_delete=models.CASCADE,
        related_name="chats"
    )
    patient = auto_prefetch.ForeignKey(
        "home.CustomUser",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    practitioner = auto_prefetch.ForeignKey(
        "practitioner.Practitioner",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    text = models.TextField()

    # def __str__(self):
    #   return f"{self.channel.name} user chat"

    def clean(self):
        if self.patient is not None:
            if self.patient != self.channel.chat.patient:
                raise ValidationError(
                    "This channel does not belong to this user/patient."
                )

        if self.practitioner is not None:
            if self.practitioner != self.channel.chat.practitioner:
                raise ValidationError(
                    "This channel does not belong to this practitioner."
                )

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["created_at"])
        ]

    @hook(AFTER_SAVE)
    @hook(AFTER_UPDATE)
    @hook(AFTER_DELETE)
    def invalidate_cache(self):
        cache.delete('user_practitioner_channel')


# class PractitionerChannelChat(TimeBasedModel):
#     channel = auto_prefetch.ForeignKey(
#         "chats.UserPractitionerChannel",
#         on_delete=models.CASCADE,
#         related_name="practitioner"
#     )
#     practitioner = auto_prefetch.ForeignKey(
#         "practitioner.Practitioner",
#         on_delete=models.CASCADE
#     )
#     text = models.TextField()

#     class Meta:
#         ordering = ["created_at"]
#         indexes = [
#             models.Index(fields=["created_at"])
#         ]

#     def clean(self):
#         if self.practitioner != self.channel.chat.practitioner:
#             raise ValidationError(
# "This channel does not belong to this user/patient.")

#     # def __str__(self):
#     #     return f"{self.channel} practitioner chat"
#     @hook(AFTER_SAVE)
#     @hook(AFTER_UPDATE)
#     @hook(AFTER_DELETE)
#     def invalidate_cache(self):
#         cache.delete('user_practitioner_channel')
