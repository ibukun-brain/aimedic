from django.contrib import admin

from appointments.models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        "patient",
        "practitioner",
        "link",
        "created_at",
        "end_date",
        "status",
        "completed",
    ]
    list_select_related = ["patient", "practitioner"]
    raw_id_fields = ["patient", "practitioner"]
    date_hierarchy = "created_at"
    search_fields = ["=patient__email", "=practitioner__email"]
    list_filter = ["status", "completed", "created_at"]
