import auto_prefetch
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django_resized import ResizedImageField

from aimedic.utils.choices import Gender, Profile
from aimedic.utils.managers import CustomUserManager
from aimedic.utils.media import MediaHelper
from aimedic.utils.models import TimeBasedModel
from aimedic.utils.validators import FileValidatorHelper


class CustomUser(TimeBasedModel, AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    # REQUIRED_FIELDS = ["first_name", "last_name"]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(verbose_name="email address", unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=15, choices=Gender.choices, blank=True)
    profile_pic = ResizedImageField(
        upload_to=MediaHelper.get_image_upload_path,
        blank=True,
        verbose_name="Profile Picture",
        validators=[
            FileValidatorHelper.validate_file_size,
            FileValidatorHelper.validate_image_extension,
        ],
    )
    type = models.TextField(
        max_length=50, choices=Profile.choices, default=Profile.Patient
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    enable_two_factor = models.BooleanField(default=False)
    objects = CustomUserManager()

    class Meta(auto_prefetch.Model.Meta):
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["date_joined"]
        indexes = [models.Index(fields=["date_joined"])]

    def get_full_name(self) -> str:
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_practitioner(self) -> bool:
        """Return true if user is a registered practitioner"""
        return hasattr(self, "practitioner")

    @property
    def image_url(self) -> str:
        if self.profile_pic:
            return self.profile_pic.url
        return ""

    @property
    def age(self) -> str:
        if self.date_of_birth:
            _age = (timezone.now().date() - self.date_of_birth) / 365
            return _age.days
        return ""

    def __str__(self):
        return self.get_full_name() or self.email
