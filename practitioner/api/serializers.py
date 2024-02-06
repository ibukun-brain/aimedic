from django.db import IntegrityError
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from chats.api.serializers import UserImageSerializer

from practitioner.models import Practitioner, PractitionerPatient


class PractitionerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Practitioner
        fields = [
            "id",
            "user",
            "office_address",
            "city",
            "state",
            "latitude",
            "longitude",
        ]
        extra_kwargs = {
            "longitude": {
                "read_only": True,
            },
            "latitude": {
                "read_only": True,
            }
        }

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
            "total_operations",
        ]


class PractitionerPatientSerializer(serializers.ModelSerializer):
    chat_id = serializers.SerializerMethodField()  # chat or channel id
    patient = UserImageSerializer(many=False)

    class Meta:
        model = PractitionerPatient
        fields = [
            "chat_id",
            "patient",
        ]

    @extend_schema_field(OpenApiTypes.UUID)
    def get_chat_id(self, obj):
        return obj.userpractitionerchannel.pk

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["details"] = data.pop("patient")
        return data
