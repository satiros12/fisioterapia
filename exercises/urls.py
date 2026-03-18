from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BodySegmentViewSet,
    BodySubSegmentViewSet,
    ExerciseCategoryViewSet,
    PathologyViewSet,
    MuscleViewSet,
    ExerciseViewSet,
)

router = DefaultRouter()
router.register(r"segments", BodySegmentViewSet, basename="segment")
router.register(r"sub-segments", BodySubSegmentViewSet, basename="subsegment")
router.register(r"categories", ExerciseCategoryViewSet, basename="category")
router.register(r"pathologies", PathologyViewSet, basename="pathology")
router.register(r"muscles", MuscleViewSet, basename="muscle")
router.register(r"exercises", ExerciseViewSet, basename="exercise")

urlpatterns = [
    path("", include(router.urls)),
]
