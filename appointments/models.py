import auto_prefetch
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.utils import timezone
from django_lifecycle import AFTER_UPDATE, LifecycleModelMixin, hook

from aimedic.utils.choices import AppointmentStatus
from aimedic.utils.models import TimeBasedModel
from chats.models import UserPractitionerChannel
from practitioner.models import PractitionerPatient


class Appointment(LifecycleModelMixin, TimeBasedModel):
    patient = auto_prefetch.ForeignKey(
        "home.CustomUser",
        on_delete=models.CASCADE,
    )
    practitioner = auto_prefetch.ForeignKey(
        "practitioner.Practitioner",
        on_delete=models.CASCADE,
        related_name="appointments",
    )
    link = models.CharField(max_length=256, blank=True)
    note = models.TextField(blank=True)
    date_booked = models.DateField(blank=True, null=True)
    # active = models.BooleanField(default=False)
    status = models.CharField(
        max_length=50,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.Pending,
    )
    completed = models.BooleanField(default=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"Appointment at {self.created_at}"

    class Meta:
        ordering = ["-date_booked", "-updated_at"]
        indexes = [models.Index(fields=["-date_booked", "-updated_at"])]
        constraints = [
            UniqueConstraint(
                name="unique_appointment",
                fields=["patient", "practitioner", "date_booked"],
                violation_error_message=(
                    "You have booked an appointment with this practitioner"
                ),
            )
        ]

    @property
    def accept_appointment(self):
        _practitioner_patient, _ = PractitionerPatient.objects.get_or_create(
            patient=self.patient, practitioner=self.practitioner
        )

    def clean(self):
        if self.practitioner.user == self.patient:
            raise ValidationError(
                "You cannot book an appointment as a practitioner"
                + "and patient the same time"
            )

    def save(self, *args, **kwargs):
        if self.start_date:
            self.date_booked = self.start_date.date()
        self.full_clean()
        super().save(*args, **kwargs)

    @hook(AFTER_UPDATE, when="completed", has_changed=True)
    def update_end_date(self):
        """This function/hook updates the end_date of appointment after completed"""
        self.updated_at = timezone.now()

    @hook(
        AFTER_UPDATE,
        when="status",
        was=AppointmentStatus.Pending,
        is_now=AppointmentStatus.Active,
    )
    def create_patient_practitioner_(self):
        """This function/hook updates when the practitioner accepts an appointment"""
        practitioner_patient, _ = PractitionerPatient.objects.get_or_create(
            practitioner=self.practitioner, patient=self.patient
        )
        _user_practitioner_channel, _ = UserPractitionerChannel.objects.get_or_create(
            chat=practitioner_patient
        )
