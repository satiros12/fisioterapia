from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("patients.urls")),
    path("api/", include("exercises.urls")),
    path("api/", include("treatments.urls")),
]
