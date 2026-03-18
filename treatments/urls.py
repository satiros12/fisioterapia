from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TreatmentPlanViewSet,
    TreatmentExerciseViewSet,
    ExerciseSessionViewSet,
    LevelProgressionViewSet,
)

router = DefaultRouter()
router.register(r"treatment-plans", TreatmentPlanViewSet, basename="treatmentplan")
router.register(
    r"treatment-exercises", TreatmentExerciseViewSet, basename="treatmentexercise"
)
router.register(r"sessions", ExerciseSessionViewSet, basename="session")
router.register(r"progressions", LevelProgressionViewSet, basename="progression")

urlpatterns = [
    path("", include(router.urls)),
]
