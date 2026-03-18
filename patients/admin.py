from django.contrib import admin
from .models import Patient, Physiotherapist


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ["user", "age", "condition", "created_at"]
    search_fields = [
        "user__username",
        "user__first_name",
        "user__last_name",
        "condition",
    ]
    list_filter = ["created_at"]


@admin.register(Physiotherapist)
class PhysiotherapistAdmin(admin.ModelAdmin):
    list_display = ["user", "license_number", "created_at"]
    search_fields = ["user__username", "user__first_name", "user__last_name"]
