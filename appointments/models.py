import auto_prefetch
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.utils import timezone
from practitioner.models import PractitionerPatient
from django.core.exceptions import ValidationError

from aimedic.utils.models import TimeBasedModel


class Appointment(TimeBasedModel):
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
    date = models.DateField(default=timezone.now)
    active = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Appointment at {self.created_at}"

    class Meta:
        ordering = ["-date", "-updated_at"]
        indexes = [
            models.Index(fields=["-date", "-updated_at"])
        ]
        constraints = [
            UniqueConstraint(
                name='unique_appointment', fields=['patient', 'practitioner', 'date'],
                violation_error_message=(
                    "You have booked an appointment with this practitioner"
                )
            )
        ]

    @property
    def accept_appointment(self):
        _practitioner_patient, _ = PractitionerPatient.objects.get_or_create(
            patient=self.patient,
            practitioner=self.practitioner
        )

    def clean(self):
        if self.practitioner.user == self.patient:
            raise ValidationError(
                "You cannot book an appointment as a practitioner" +
                "and patient the same time"
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
