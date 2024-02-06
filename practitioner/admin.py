from django.contrib import admin

from practitioner.models import Practitioner, PractitionerOperation, PractitionerPatient


@admin.register(Practitioner)
class PractionerAdmin(admin.ModelAdmin):
    list_display = ["user", "created_at"]
    raw_id_fields = ["user"]
    search_fields = ["user__first_name", "user__last_name", "user__email"]
    list_select_related = ["user"]
    list_filter = ["created_at"]


@admin.register(PractitionerPatient)
class PractitionerPatientAdmin(admin.ModelAdmin):
    list_display = ["practitioner", "patient", "created_at"]
    raw_id_fields = ["practitioner", "patient"]
    search_fields = ["practitioner__email"]
    list_filter = ["created_at"]


@admin.register(PractitionerOperation)
class PractitionerOperationAdmin(admin.ModelAdmin):
    list_display = ["practitioner", "patient", "created_at"]
    raw_id_fields = ["practitioner", "patient"]
    search_fields = ["practitioner__email", "patient__email"]
    list_filter = ["created_at"]
