from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient")
    age = models.PositiveIntegerField(null=True, blank=True)
    condition = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"


class Physiotherapist(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="physiotherapist"
    )
    license_number = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PT: {self.user.get_full_name() or self.user.username}"
