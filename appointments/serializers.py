from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    DailyExerciseRecord,
    ExerciseStatus,
    ProfessionalSchedule,
    DayOff,
    Appointment,
    AppointmentStatus,
    Message,
)


class UserSimpleSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "name"]

    def get_name(self, obj):
        return obj.get_full_name() or obj.username


class DailyExerciseRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()

    class Meta:
        model = DailyExerciseRecord
        fields = [
            "id",
            "patient",
            "patient_name",
            "treatment_exercise_id",
            "exercise_name",
            "date",
            "status",
            "comments",
            "created_at",
            "updated_at",
        ]

    def get_patient_name(self, obj):
        return obj.patient.get_full_name() or obj.patient.username


class DailyExerciseRecordCreateSerializer(serializers.Serializer):
    treatment_exercise_id = serializers.IntegerField()
    exercise_name = serializers.CharField()
    date = serializers.DateField()
    status = serializers.ChoiceField(choices=ExerciseStatus.choices)
    comments = serializers.CharField(required=False, allow_blank=True)


class ProfessionalScheduleSerializer(serializers.ModelSerializer):
    day_name = serializers.CharField(source="get_day_of_week_display", read_only=True)
    day_of_week = serializers.IntegerField(min_value=0, max_value=6)

    class Meta:
        model = ProfessionalSchedule
        fields = [
            "id",
            "physiotherapist",
            "day_of_week",
            "day_name",
            "start_time",
            "end_time",
            "is_active",
        ]


class DayOffSerializer(serializers.ModelSerializer):
    date = serializers.DateField()

    class Meta:
        model = DayOff
        fields = ["id", "physiotherapist", "date", "reason"]


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    physiotherapist_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id",
            "patient",
            "patient_name",
            "physiotherapist",
            "physiotherapist_name",
            "date",
            "start_time",
            "end_time",
            "status",
            "status_display",
            "patient_notes",
            "professional_notes",
            "created_at",
            "updated_at",
        ]

    def get_patient_name(self, obj):
        return obj.patient.get_full_name() or obj.patient.username

    def get_physiotherapist_name(self, obj):
        return obj.physiotherapist.get_full_name() or obj.physiotherapist.username


class AppointmentCreateSerializer(serializers.Serializer):
    physiotherapist_id = serializers.IntegerField()
    date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    patient_notes = serializers.CharField(required=False, allow_blank=True)


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    recipient_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "id",
            "sender",
            "sender_name",
            "recipient",
            "recipient_name",
            "subject",
            "body",
            "is_read",
            "created_at",
        ]

    def get_sender_name(self, obj):
        return obj.sender.get_full_name() or obj.sender.username

    def get_recipient_name(self, obj):
        return obj.recipient.get_full_name() or obj.recipient.username


class MessageCreateSerializer(serializers.Serializer):
    recipient_id = serializers.IntegerField()
    subject = serializers.CharField()
    body = serializers.CharField()
