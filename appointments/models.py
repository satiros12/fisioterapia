from django.db import models
from django.conf import settings


class ExerciseStatus(models.TextChoices):
    NOTHING = "nothing", "Sin hacer"
    COMPLETE = "complete", "Completado"
    OVERDONE = "overdone", "Excedido"
    INCOMPLETE = "incomplete", "Incompleto"


class DailyExerciseRecord(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="daily_exercise_records",
    )
    treatment_exercise_id = models.PositiveIntegerField()
    exercise_name = models.CharField(max_length=200)
    date = models.DateField()
    status = models.CharField(
        max_length=20, choices=ExerciseStatus.choices, default=ExerciseStatus.NOTHING
    )
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["patient", "treatment_exercise_id", "date"]
        ordering = ["-date", "exercise_name"]

    def __str__(self):
        return f"{self.exercise_name} - {self.date} - {self.status}"


class ProfessionalSchedule(models.Model):
    physiotherapist = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="schedules"
    )
    day_of_week = models.PositiveIntegerField(
        choices=[
            (0, "Lunes"),
            (1, "Martes"),
            (2, "Miércoles"),
            (3, "Jueves"),
            (4, "Viernes"),
            (5, "Sábado"),
            (6, "Domingo"),
        ]
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["day_of_week", "start_time"]

    def __str__(self):
        return f"{self.get_day_of_week_display()} {self.start_time}-{self.end_time}"


class DayOff(models.Model):
    physiotherapist = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="days_off"
    )
    date = models.DateField()
    reason = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Day off: {self.date}"


class AppointmentStatus(models.TextChoices):
    PENDING = "pending", "Pendiente"
    ACCEPTED = "accepted", "Aceptada"
    DENIED = "denied", "Denegada"
    COMPLETED = "completed", "Completada"
    CANCELLED = "cancelled", "Cancelada"


class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages",
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_messages",
    )
    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.sender} -> {self.recipient}: {self.subject}"


class Appointment(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="appointments"
    )
    physiotherapist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_appointments",
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.PENDING,
    )
    patient_notes = models.TextField(blank=True)
    professional_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["date", "start_time"]
        unique_together = ["physiotherapist", "date", "start_time"]

    def __str__(self):
        return f"{self.date} {self.start_time} - {self.patient}"
