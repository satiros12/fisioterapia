from django.db import models
from django.conf import settings


class TreatmentPlan(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="treatment_plans",
    )
    physiotherapist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_plans",
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Plan: {self.name} - {self.patient}"


class TreatmentExercise(models.Model):
    treatment_plan = models.ForeignKey(
        TreatmentPlan, on_delete=models.CASCADE, related_name="exercises"
    )
    exercise_id = models.PositiveIntegerField()
    exercise_name = models.CharField(max_length=200)

    assigned_level = models.PositiveIntegerField(default=1)
    current_level = models.PositiveIntegerField(default=1)

    notes = models.TextField(blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["assigned_at"]

    def __str__(self):
        return f"{self.exercise_name} - Level {self.current_level}"


class ExerciseSession(models.Model):
    treatment_exercise = models.ForeignKey(
        TreatmentExercise, on_delete=models.CASCADE, related_name="sessions"
    )

    eva_before = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="EVA antes del ejercicio"
    )
    eva_after = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="EVA después del ejercicio"
    )

    is_completed = models.BooleanField(default=False)
    completion_notes = models.TextField(blank=True)

    session_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session: {self.treatment_exercise.exercise_name} - {self.session_date.date()}"

    @property
    def can_advance_level(self):
        return self.eva_after is not None and self.eva_after <= 6


class LevelProgression(models.Model):
    treatment_exercise = models.ForeignKey(
        TreatmentExercise, on_delete=models.CASCADE, related_name="progressions"
    )
    from_level = models.PositiveIntegerField()
    to_level = models.PositiveIntegerField()
    progressed_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True)

    def __str__(self):
        return f"Level {self.from_level} -> {self.to_level}"
