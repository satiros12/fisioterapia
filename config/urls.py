from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import index, exercises_view, treatment_plans_view, exercise_detail_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("patients.urls")),
    path("api/", include("exercises.urls")),
    path("api/", include("treatments.urls")),
    path("", index, name="index"),
    path("ejercicios", exercises_view, name="exercises"),
    path("planes", treatment_plans_view, name="treatment_plans"),
    path("ejercicio/<int:exercise_id>", exercise_detail_view, name="exercise_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
