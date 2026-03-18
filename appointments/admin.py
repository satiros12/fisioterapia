from django.contrib import admin
from .models import DailyExerciseRecord, ProfessionalSchedule, DayOff, Appointment


@admin.register(DailyExerciseRecord)
class DailyExerciseRecordAdmin(admin.ModelAdmin):
    list_display = ["patient", "exercise_name", "date", "status", "created_at"]
    list_filter = ["status", "date"]
    search_fields = ["patient__username", "exercise_name"]


@admin.register(ProfessionalSchedule)
class ProfessionalScheduleAdmin(admin.ModelAdmin):
    list_display = [
        "physiotherapist",
        "day_of_week",
        "start_time",
        "end_time",
        "is_active",
    ]
    list_filter = ["is_active", "day_of_week"]


@admin.register(DayOff)
class DayOffAdmin(admin.ModelAdmin):
    list_display = ["physiotherapist", "date", "reason"]
    list_filter = ["date"]


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["patient", "physiotherapist", "date", "start_time", "status"]
    list_filter = ["status", "date"]
    search_fields = ["patient__username", "physiotherapist__username"]
