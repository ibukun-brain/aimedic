import auto_prefetch

# from django.core.cache import cache
from django.db import models
from django.forms import ValidationError

from aimedic.utils.models import TimeBasedModel

# from django_lifecycle import (
#     AFTER_DELETE,
#     AFTER_SAVE,
#     AFTER_UPDATE,
#     LifecycleModelMixin,
#     hook,
# )


class Practitioner(TimeBasedModel):
    user = auto_prefetch.OneToOneField("home.CustomUser", on_delete=models.CASCADE)
    office_address = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=256, blank=True)
    state = models.CharField(max_length=256, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.user)

    class Meta(auto_prefetch.Model.Meta):
        ordering = ["-created_at", "user__first_name", "user__last_name"]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]

    @property
    def total_appointments(self) -> int:
        return self.appointments.count()

    @property
    def total_patients(self) -> int:
        return self.patients.all().count()

    @property
    def total_operations(self) -> int:
        return self.operations.count()


class PractitionerPatient(TimeBasedModel):
    # patients = auto_prefetch.ForeignKey(
    #     "home.CustomUser",
    #     on_delete=models.CASCADE
    # )
    practitioner = auto_prefetch.ForeignKey(
        "practitioner.Practitioner",
        on_delete=models.CASCADE,
        related_name="practitioner_patient",
    )
    patient = auto_prefetch.ForeignKey(
        "home.CustomUser", on_delete=models.CASCADE, related_name="practitioner_patient"
    )

    class Meta(auto_prefetch.Model.Meta):
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return f"Dr. {self.practitioner} x {self.patient}"

    # @hook(AFTER_SAVE)
    # @hook(AFTER_UPDATE)
    # @hook(AFTER_DELETE)
    # def invalidate_cache(self):
    #     cache.delete("patient_list")
    #     cache.delete("practitioner_list")

    def clean(self):
        if self.practitioner.user == self.patient:
            raise ValidationError(
                "You cannot be a practioner and a patient to yourself"
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class PractitionerOperation(TimeBasedModel):
    practitioner = auto_prefetch.ForeignKey(
        "practitioner.Practitioner", on_delete=models.CASCADE, related_name="operations"
    )
    patient = auto_prefetch.ForeignKey(
        "home.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="operations",
    )
    log = models.TextField(blank=True)
    successful = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.practitioner} Operation"

    class Meta(auto_prefetch.Model.Meta):
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]
