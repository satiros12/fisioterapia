from django.contrib import admin
from .models import TreatmentPlan, TreatmentExercise, ExerciseSession, LevelProgression


@admin.register(TreatmentPlan)
class TreatmentPlanAdmin(admin.ModelAdmin):
    list_display = ["name", "patient", "physiotherapist", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "patient__username"]


@admin.register(TreatmentExercise)
class TreatmentExerciseAdmin(admin.ModelAdmin):
    list_display = [
        "exercise_name",
        "treatment_plan",
        "assigned_level",
        "current_level",
        "assigned_at",
    ]
    list_filter = ["assigned_level", "current_level"]
    search_fields = ["exercise_name", "treatment_plan__name"]


@admin.register(ExerciseSession)
class ExerciseSessionAdmin(admin.ModelAdmin):
    list_display = [
        "treatment_exercise",
        "eva_before",
        "eva_after",
        "is_completed",
        "session_date",
    ]
    list_filter = ["is_completed", "session_date"]
    search_fields = ["treatment_exercise__exercise_name"]


@admin.register(LevelProgression)
class LevelProgressionAdmin(admin.ModelAdmin):
    list_display = ["treatment_exercise", "from_level", "to_level", "progressed_at"]
    list_filter = ["progressed_at"]
