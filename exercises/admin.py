from django.contrib import admin
from .models import (
    BodySegment,
    BodySubSegment,
    ExerciseCategory,
    Pathology,
    Muscle,
    Exercise,
)


@admin.register(BodySegment)
class BodySegmentAdmin(admin.ModelAdmin):
    list_display = ["name", "name_es", "created_at"]
    search_fields = ["name", "name_es"]


@admin.register(BodySubSegment)
class BodySubSegmentAdmin(admin.ModelAdmin):
    list_display = ["name", "name_es", "segment"]
    list_filter = ["segment"]
    search_fields = ["name", "name_es"]


@admin.register(ExerciseCategory)
class ExerciseCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "name_es"]


@admin.register(Pathology)
class PathologyAdmin(admin.ModelAdmin):
    list_display = ["name", "name_es"]
    filter_horizontal = ["affected_segments"]


@admin.register(Muscle)
class MuscleAdmin(admin.ModelAdmin):
    list_display = ["name", "name_es"]
    filter_horizontal = ["sub_segments"]


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ["name", "sub_segment", "category", "level", "is_active"]
    list_filter = ["category", "level", "is_active", "sub_segment__segment"]
    search_fields = ["name", "description"]
    filter_horizontal = ["pathologies", "muscles"]
