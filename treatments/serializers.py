from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TreatmentPlan, TreatmentExercise, ExerciseSession, LevelProgression


class UserSimpleSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "name"]

    def get_name(self, obj):
        return obj.get_full_name() or obj.username


class TreatmentPlanSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    physiotherapist_name = serializers.SerializerMethodField()
    exercises_count = serializers.SerializerMethodField()

    class Meta:
        model = TreatmentPlan
        fields = [
            "id",
            "patient",
            "patient_name",
            "physiotherapist",
            "physiotherapist_name",
            "name",
            "description",
            "start_date",
            "end_date",
            "is_active",
            "exercises_count",
            "created_at",
            "updated_at",
        ]

    def get_patient_name(self, obj):
        return obj.patient.get_full_name() or obj.patient.username

    def get_physiotherapist_name(self, obj):
        if obj.physiotherapist:
            return obj.physiotherapist.get_full_name() or obj.physiotherapist.username
        return None

    def get_exercises_count(self, obj):
        return obj.exercises.count()


class TreatmentPlanCreateSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    start_date = serializers.DateField(required=False, allow_null=True)
    end_date = serializers.DateField(required=False, allow_null=True)


class TreatmentExerciseSerializer(serializers.ModelSerializer):
    exercise_details = serializers.SerializerMethodField()

    class Meta:
        model = TreatmentExercise
        fields = [
            "id",
            "treatment_plan",
            "exercise_id",
            "exercise_name",
            "exercise_details",
            "assigned_level",
            "current_level",
            "notes",
            "assigned_at",
        ]

    def get_exercise_details(self, obj):
        from exercises.models import Exercise

        try:
            exercise = Exercise.objects.get(id=obj.exercise_id)
            from exercises.serializers import ExerciseSerializer

            return ExerciseSerializer(exercise).data
        except Exercise.DoesNotExist:
            return None


class ExerciseSessionSerializer(serializers.ModelSerializer):
    can_advance = serializers.BooleanField(read_only=True)
    session_date_formatted = serializers.DateTimeField(
        source="session_date", read_only=True, format="%Y-%m-%d %H:%M"
    )

    class Meta:
        model = ExerciseSession
        fields = [
            "id",
            "treatment_exercise",
            "eva_before",
            "eva_after",
            "is_completed",
            "completion_notes",
            "session_date",
            "session_date_formatted",
            "can_advance",
        ]


class LevelProgressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelProgression
        fields = [
            "id",
            "treatment_exercise",
            "from_level",
            "to_level",
            "progressed_at",
            "reason",
        ]


class RecordSessionSerializer(serializers.Serializer):
    treatment_exercise_id = serializers.IntegerField()
    eva_before = serializers.IntegerField(min_value=0, max_value=10, required=False)
    eva_after = serializers.IntegerField(min_value=0, max_value=10, required=False)
    is_completed = serializers.BooleanField(default=False)
    completion_notes = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        if data.get("is_completed") and data.get("eva_after") is None:
            raise serializers.ValidationError(
                "EVA after is required when marking as completed"
            )
        return data
