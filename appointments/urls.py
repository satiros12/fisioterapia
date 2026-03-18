from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DailyExerciseRecordViewSet,
    ProfessionalScheduleViewSet,
    DayOffViewSet,
    AppointmentViewSet,
    MessageViewSet,
)

router = DefaultRouter()
router.register(
    r"daily-exercises", DailyExerciseRecordViewSet, basename="dailyexercise"
)
router.register(r"schedule", ProfessionalScheduleViewSet, basename="schedule")
router.register(r"days-off", DayOffViewSet, basename="daysoff")
router.register(r"appointments", AppointmentViewSet, basename="appointment")
router.register(r"messages", MessageViewSet, basename="message")

urlpatterns = [
    path("", include(router.urls)),
]
