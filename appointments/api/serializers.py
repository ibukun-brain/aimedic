from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils import timezone

# from drf_spectacular.types import OpenApiTypes
# from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from aimedic.utils.choices import AppointmentDurationStatus, AppointmentStatus
from appointments.models import Appointment

# from practitioner.api.serializers import PractitionerSerializer


class PatientCreateAppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()
    practitioner = serializers.StringRelatedField()
    duration = serializers.ChoiceField(
        choices=AppointmentDurationStatus.choices,
        write_only=True,
        help_text="Duration in hours",
    )

    class Meta:
        model = Appointment
        fields = [
            "patient",
            "practitioner",
            "duration",
            "start_date",
        ]

    def validate_start_date(self, value):
        start_date = value.date()
        if start_date < datetime.now().date():
            raise serializers.ValidationError("start_date cannot less than today")
        return value

    def create(self, validated_data):
        end_date = validated_data.get("start_date") + timezone.timedelta(
            hours=validated_data.get("duration")
        )
        try:
            return Appointment.objects.create(
                patient=validated_data.get("patient"),
                practitioner=validated_data.get("practitioner"),
                start_date=validated_data.get("start_date"),
                end_date=end_date,
            )
        except ValidationError as e:
            raise serializers.ValidationError(
                {"error": "You cannot create multiple appointment on the same day"}
            ) from e


class PatientAppointmentSerializer(serializers.ModelSerializer):
    # patient = serializers.HiddenField(default=serializers.CurrentUserDefault())
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
            # "patient",
            "id",
            "practitioner",
            "link",
            "start_date",
            "end_date",
            # "time",
            "note",
            "status",
            "completed",
        ]
        extra_kwargs = {
            "status": {
                "read_only": True,
            },
            "completed": {
                "read_only": True,
            },
        }


class PractitionerAcceptOrDeclineAppointmentSerializer(serializers.ModelSerializer):
    appointment_id = serializers.HiddenField(default="")
    practitioner = serializers.StringRelatedField(read_only=True)
    patient = serializers.StringRelatedField(read_only=True)
    accept = serializers.BooleanField(
        help_text="Accept or decline appointments", write_only=True
    )

    class Meta:
        model = Appointment
        fields = [
            "appointment_id",
            "practitioner",
            "patient",
            "status",
            "accept",
            "created_at",
        ]
        extra_kwargs = {
            "status": {
                "read_only": True,
            },
            "end_date": {
                "read_only": True,
            },
        }

    def create(self, validated_data):
        appointment, created = Appointment.objects.get_or_create(
            id=validated_data.get("appointment_id"),
            patient=validated_data.get("patient"),
            practitioner=validated_data.get("practitioner"),
        )
        if not created:
            if validated_data.get("accept"):
                appointment.status = AppointmentStatus.Active
                appointment.save()
            else:
                appointment.status = AppointmentStatus.Cancelled
                appointment.save()

        return appointment

    # def update(self, instance, validated_data):
    #     accept = validated_data.get("accept")
    #     patient = validated_data.get("patient")
    #     practitioner = self.context["request"].user.practitioner
    #     if accept:
    #         try:
    #             instance.accept_appointment
    #         except ValidationError as e:
    #             raise serializers.ValidationError(
    #                 {"error": "You cannot be a practioner and a patient to yourself"}
    #             ) from e
    #         return {
    #             "success": True,
    #             "patient": patient,
    #             "accept": accept,
    #             "message": "Appointment accepted",
    #         }

    #     appointment = Appointment.objects.select_related("patient", "practitioner").
    # get(
    #         patient=patient,
    #         practitioner=practitioner,
    #     )
    #     appointment.status = False
    #     appointment.save()
    #     return {"success": True, "message": "Appointment declined"}


class PractitionerAppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()
    # time = serializers.SerializerMethodField()
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
            # "date",
            # "time",
            "created_at",
            "status",
            "completed",
            "accept",
        ]
        extra_kwargs = {
            "status": {
                "read_only": False,
            },
            "completed": {
                "read_only": False,
            },
        }

    # @extend_schema_field(OpenApiTypes.TIME)
    # def get_time(self, obj):
    #     if obj.updated_at:
    #         return obj.updated_at.strftime("%H:%M")
    #     return obj.created_at.strftime("%H:%M")
