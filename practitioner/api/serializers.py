from django.contrib.auth import get_user_model
from django.db import IntegrityError
from djoser.serializers import UserCreateSerializer
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from chats.api.serializers import UserImageSerializer
from home.models import CustomUser
from practitioner.models import Practitioner, PractitionerPatient

User = get_user_model()


class PractitionerCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = [
            "first_name",
            "last_name",
            "type",
            # "date_of_birth",
            "email",
            "gender",
            "password",
        ]

    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data, type="practitioner")
        _practitioner, _ = Practitioner.objects.get_or_create(user=user)
        return user


class PractitionerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.get_full_name")
    image = serializers.CharField(source="user.profile_pic")
    gender = serializers.CharField(source="user.gender")
    email = serializers.CharField(source="user.email")

    class Meta:
        model = Practitioner
        fields = [
            "id",
            "name",
            "email",
            "gender",
            "image",
            "office_address",
            "city",
            "state",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data

    def create(self, validated_data):
        try:
            Practitioner.objects.create(**validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError(
                {"error": "You are already a practitioner"}
            ) from e


class PractitionerOverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practitioner
        fields = [
            "total_appointments",
            "total_patients",
        ]


class PractitionerPatientSerializer(serializers.ModelSerializer):
    chat_id = serializers.SerializerMethodField()  # chat or channel id
    patient = UserImageSerializer(many=False)
    recent_message = serializers.SerializerMethodField()

    class Meta:
        model = PractitionerPatient
        fields = [
            "chat_id",
            "patient",
            "recent_message",
        ]

    @extend_schema_field(OpenApiTypes.UUID)
    def get_chat_id(self, obj):
        return obj.userpractitionerchannel.pk

    def get_recent_message(self, obj):
        return obj.userpractitionerchannel.patient_recent_message

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # data["details"] = data.pop("patient")
        return data
