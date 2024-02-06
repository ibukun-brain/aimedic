from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class OrderField(models.PositiveIntegerField):
    def __init__(self, *args, for_fields=None, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            qs = self.model.objects.all()
            if self.for_fields:
                # filter by objects with the same field values
                # for the fields in "for_fields"
                query = {
                    field: getattr(model_instance, field) for field in self.for_fields
                }
                qs = qs.filter(**query)
                # get the order of the last item

            try:
                last_item = qs.latest(self.attname)
            except ObjectDoesNotExist:
                value = 1
                setattr(model_instance, self.attname, value)
                return value
            value = last_item.order + 1
            return value
        return super().pre_save(model_instance, add)
