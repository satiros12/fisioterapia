from rest_framework import serializers
from .models import (
    BodySegment,
    BodySubSegment,
    ExerciseCategory,
    Pathology,
    Muscle,
    Exercise,
)


class BodySegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodySegment
        fields = ["id", "name", "name_es", "atlas_image", "description"]


class BodySubSegmentSerializer(serializers.ModelSerializer):
    segment_name = serializers.CharField(source="segment.name", read_only=True)
    atlas_image_url = serializers.SerializerMethodField()

    class Meta:
        model = BodySubSegment
        fields = [
            "id",
            "segment",
            "segment_name",
            "name",
            "name_es",
            "atlas_image",
            "atlas_image_url",
            "description",
        ]

    def get_atlas_image_url(self, obj):
        if obj.atlas_image:
            return obj.atlas_image.url
        return None


class ExerciseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseCategory
        fields = ["id", "name", "name_es", "description"]


class PathologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pathology
        fields = ["id", "name", "name_es", "description", "affected_segments"]


class MuscleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Muscle
        fields = ["id", "name", "name_es", "sub_segments"]


class ExerciseSerializer(serializers.ModelSerializer):
    sub_segment_name = serializers.CharField(source="sub_segment.name", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    category_name_es = serializers.CharField(source="category.name_es", read_only=True)
    segment_name = serializers.CharField(
        source="sub_segment.segment.name", read_only=True
    )
    reference_image_url = serializers.SerializerMethodField()
    muscle_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = [
            "id",
            "sub_segment",
            "sub_segment_name",
            "segment_name",
            "category",
            "category_name",
            "category_name_es",
            "level",
            "name",
            "description",
            "instructions",
            "reference_image",
            "reference_image_url",
            "muscle_image_url",
            "pathologies",
            "muscles",
            "is_active",
            "created_at",
        ]

    def get_reference_image_url(self, obj):
        if obj.reference_image:
            return obj.reference_image.url
        return None

    def get_muscle_image_url(self, obj):
        if obj.muscle_image:
            return obj.muscle_image.url
        return None


class ExerciseListSerializer(serializers.ModelSerializer):
    category_name_es = serializers.CharField(source="category.name_es", read_only=True)
    level_name = serializers.CharField(source="get_level_display", read_only=True)
    reference_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = [
            "id",
            "name",
            "description",
            "category_name_es",
            "level",
            "level_name",
            "reference_image_url",
        ]

    def get_reference_image_url(self, obj):
        if obj.reference_image:
            return obj.reference_image.url
        return None
