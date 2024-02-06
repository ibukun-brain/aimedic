from django.core.exceptions import ValidationError
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers, validators

from appointments.models import Appointment


class PatientCreateAppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    practitioner = serializers.StringRelatedField()
    date = serializers.DateField()

    class Meta:
        model = Appointment
        fields = [
            "patient",
            "practitioner",
            "date",
            # "time",
        ]
    validators = [
        validators.UniqueForDateValidator(
            queryset=Appointment.objects.select_related(
                "patient",
                "practitioner",
            ).all(),
            field="patient",
            date_field="date",
            message="You have booked an appointment with this practitioner"
        )
    ]


class PatientAppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    practitioner = serializers.StringRelatedField()
    # time = serializers.SerializerMethodField()

    # @extend_schema_field(OpenApiTypes.TIME)
    # def get_time(self, obj):
    #     if obj.updated_at:
    #         return obj.updated_at.strftime("%H:%M")
    #     return obj.created_at.strftime("%H:%M")

    class Meta:
        model = Appointment
        fields = [
            "patient",
            "practitioner",
            "link",
            "created_at",
            # "time",
            "note",
            "active",
            "completed",
        ]
        extra_kwargs = {
            "active": {
                "read_only": True,
            },
            "completed": {
                "read_only": True,
            },
            "date": {
                "read_only": True,
            }
        }


class PractitionerAcceptAppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()
    accept = serializers.BooleanField(
        help_text="Accept or decline appointments",
    )

    class Meta:
        model = Appointment
        fields = [
            "patient",
            "accept",
        ]

    def update(self, instance, validated_data):
        accept = validated_data.get("accept")
        patient = validated_data.get("patient")
        practitioner = self.context["request"].user.practitioner
        if accept:
            try:
                instance.accept_appointment
            except ValidationError:
                raise serializers.ValidationError(
                    {"error": "You cannot be a practioner and a patient to yourself"}
                )
            return {
                "success": True,
                "patient": patient,
                "accept": accept,
                "message": "Appointment accepted",
            }

        else:
            appointment = Appointment.objects.select_related("patient", "practitioner").get(
                patient=patient,
                practitioner=practitioner,
            )
            appointment.active = False
            appointment.save()
            return {
                "success": True,
                "message": "Appointment declined"
            }


class PractitionerAppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()
    time = serializers.SerializerMethodField()
    accept = serializers.BooleanField(
        help_text="Accept or decline appointments",
        write_only=True,
    )

    class Meta:
        model = Appointment
        fields = [
            "id",
            "patient",
            "link",
            "date",
            "time",
            # "created_at",
            "active",
            "completed",
            "accept"
        ]
        extra_kwargs = {
            "active": {
                "read_only": False,
            },
            "completed": {
                "read_only": False,
            }
        }

    @extend_schema_field(OpenApiTypes.TIME)
    def get_time(self, obj):
        if obj.updated_at:
            return obj.updated_at.strftime("%H:%M")
        return obj.created_at.strftime("%H:%M")
