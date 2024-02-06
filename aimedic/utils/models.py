import uuid

import auto_prefetch
from django.db import models
from django.utils.text import slugify

from aimedic.utils.managers import VisibleManager


class TimeBasedModel(auto_prefetch.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(auto_prefetch.Model.Meta):
        abstract = True

    objects = auto_prefetch.Manager()
    items = VisibleManager()


class NamedTimeBasedModel(TimeBasedModel):
    name = models.CharField(max_length=200)

    class Meta(auto_prefetch.Model.Meta):
        abstract = True
        ordering = ["name", "created_at"]

    def __str__(self):
        return self.name

    def title(self):
        """alias for `name` field"""
        return self.name


class CategoryModel(TimeBasedModel):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(null=True, blank=True, max_length=250)

    class Meta(auto_prefetch.Model.Meta):
        indexes = [
            models.Index(fields=("name",)),
        ]
        ordering = ["name", "created_at"]
        verbose_name_plural = "categories"
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
