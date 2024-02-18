from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify

from aimedic.utils.choices import AppointmentStatus
from appointments.models import Appointment
from home.tasks import send_email_task


@receiver(post_save, sender=Appointment)
def appointment_notification(sender, instance, created, **kwargs):
    if instance.status == AppointmentStatus.Pending:
        notify.send(
            sender=instance.patient,
            recipient=instance.practitioner.user,
            target=instance,
            verb="Appointment schedule",
            description=f"An appointment was sent to you by {instance.patient}",
            level="info",
        )
        send_email_task(
            subject="Pending Appointment",
            message=f"Hi Dr. {instance.practitioner.user}, a patient scheduled"
            + "an appointment with you, you can choose to accept or decline"
            ""
            "this appointment",
            email=instance.practitioner.user.email,
            otp=None,
        )

    elif instance.status == AppointmentStatus.Cancelled:
        notify.send(
            sender=instance.practitioner,
            recipient=instance.patient,
            target=instance,
            verb="Appointment cancelled",
            description="Your appointment was cancelled",
            level="warning",
        )

    elif instance.status == AppointmentStatus.Active:
        notify.send(
            sender=instance.practitioner,
            recipient=instance.patient,
            target=instance,
            verb="Appointment accepted",
            description=f"Dr. {instance.practitioner} accepted your appointment",
            level="success",
        )

    else:
        # Appointment expired
        notify.send(
            sender=instance.practitioner,
            recipient=instance.patient,
            target=instance,
            verb="Appointment expired",
            description="Your appointment date has passed and it was not attended to",
            level="success",
        )
