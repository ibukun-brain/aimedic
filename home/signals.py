# from django.db.models.signals import post_save
# from django.dispatch import receiver

# from aimedic.utils.choices import Profile
# from home.models import CustomUser
# from practitioner.models import Practitioner, PractitionerPatient


# @receiver(post_save, sender=CustomUser)
# def create_practitioner_profile(instance, created, *args, **kwargs):
#     if created:
#         if instance.type == Profile.Practitioner:
#             practitioner = Practitioner.objects.create(user=instance)
#             PractitionerPatient.objects.create(practitioner=practitioner)
