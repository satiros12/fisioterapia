from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, PhysiotherapistViewSet

router = DefaultRouter()
router.register(r"patients", PatientViewSet, basename="patient")
router.register(r"physiotherapists", PhysiotherapistViewSet, basename="physiotherapist")

urlpatterns = [
    path("", include(router.urls)),
]
