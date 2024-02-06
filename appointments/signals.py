from django.db.models.signals import post_save
from django.dispatch import receiver

from appointments.models import Appointment
from chats.models import UserPractitionerChannel
from practitioner.models import PractitionerPatient


@receiver(post_save, sender=Appointment)
def create_practitioner_patient(instance, created, *args, **kwargs):
    if created:
        practitioner_patient, _ = PractitionerPatient.objects.get_or_create(
            practitioner=instance.practitioner, patient=instance.patient
        )
        _user_practitioner_channel, _ = UserPractitionerChannel.objects.get_or_create(
            chat=practitioner_patient
        )
