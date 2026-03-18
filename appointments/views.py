from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import (
    DailyExerciseRecord,
    ProfessionalSchedule,
    DayOff,
    Appointment,
    AppointmentStatus,
    Message,
)
from .serializers import (
    DailyExerciseRecordSerializer,
    DailyExerciseRecordCreateSerializer,
    ProfessionalScheduleSerializer,
    DayOffSerializer,
    AppointmentSerializer,
    AppointmentCreateSerializer,
    MessageSerializer,
)


class DailyExerciseRecordViewSet(viewsets.ModelViewSet):
    serializer_class = DailyExerciseRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # If physiotherapist, get all patients' records
        if hasattr(user, "physiotherapist") and user.physiotherapist:
            return DailyExerciseRecord.objects.all().order_by("-date")
        # If patient, get only their records
        return DailyExerciseRecord.objects.filter(patient=user).order_by("-date")

    @action(detail=False, methods=["get"])
    def by_date(self, request):
        date_str = request.query_params.get("date")
        if not date_str:
            return Response({"detail": "date is required"}, status=400)

        records = self.get_queryset().filter(date=date_str)
        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def calendar(self, request):
        # Get records for a date range
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        queryset = self.get_queryset()
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        # Group by date
        records = queryset.order_by("date")
        calendar_data = {}
        for record in records:
            date_str = str(record.date)
            if date_str not in calendar_data:
                calendar_data[date_str] = []
            calendar_data[date_str].append(
                {
                    "id": record.id,
                    "exercise_name": record.exercise_name,
                    "status": record.status,
                    "treatment_exercise_id": record.treatment_exercise_id,
                }
            )

        return Response(calendar_data)

    def create(self, request):
        serializer = DailyExerciseRecordCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        patient = request.user

        record, created = DailyExerciseRecord.objects.update_or_create(
            patient=patient,
            treatment_exercise_id=data["treatment_exercise_id"],
            date=data["date"],
            defaults={
                "exercise_name": data["exercise_name"],
                "status": data["status"],
                "comments": data.get("comments", ""),
            },
        )

        return Response(
            DailyExerciseRecordSerializer(record).data, status=status.HTTP_201_CREATED
        )


class ProfessionalScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ProfessionalScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "physiotherapist") and user.physiotherapist:
            return ProfessionalSchedule.objects.filter(physiotherapist=user)
        return ProfessionalSchedule.objects.none()

    def perform_create(self, serializer):
        serializer.save(physiotherapist=self.request.user)


class DayOffViewSet(viewsets.ModelViewSet):
    serializer_class = DayOffSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "physiotherapist") and user.physiotherapist:
            return DayOff.objects.filter(physiotherapist=user)
        return DayOff.objects.none()

    def perform_create(self, serializer):
        serializer.save(physiotherapist=self.request.user)


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # If physiotherapist, get all appointments with their patients
        if hasattr(user, "physiotherapist") and user.physiotherapist:
            return Appointment.objects.filter(physiotherapist=user).order_by(
                "-date", "-start_time"
            )
        # If patient, get only their appointments
        return Appointment.objects.filter(patient=user).order_by("-date", "-start_time")

    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = AppointmentStatus.ACCEPTED
        appointment.save()
        return Response(AppointmentSerializer(appointment).data)

    @action(detail=True, methods=["post"])
    def deny(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = AppointmentStatus.DENIED
        appointment.professional_notes = request.data.get("reason", "")
        appointment.save()
        return Response(AppointmentSerializer(appointment).data)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = AppointmentStatus.COMPLETED
        appointment.professional_notes = request.data.get("notes", "")
        appointment.save()
        return Response(AppointmentSerializer(appointment).data)

    @action(detail=False, methods=["get"])
    def available_slots(self, request):
        physiotherapist_id = request.query_params.get("physiotherapist_id")
        date_str = request.query_params.get("date")

        if not physiotherapist_id or not date_str:
            return Response(
                {"detail": "physiotherapist_id and date are required"}, status=400
            )

        from datetime import datetime

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"detail": "Invalid date format"}, status=400)

        day_of_week = date.weekday()

        # Get schedule for this day
        schedules = ProfessionalSchedule.objects.filter(
            physiotherapist_id=physiotherapist_id,
            day_of_week=day_of_week,
            is_active=True,
        )

        # Check if it's a day off
        is_day_off = DayOff.objects.filter(
            physiotherapist_id=physiotherapist_id, date=date
        ).exists()

        if is_day_off or not schedules.exists():
            return Response(
                {"available": False, "slots": [], "reason": "Día no disponible"}
            )

        # Get existing appointments for this date
        booked = Appointment.objects.filter(
            physiotherapist_id=physiotherapist_id,
            date=date,
            status__in=[AppointmentStatus.PENDING, AppointmentStatus.ACCEPTED],
        ).values_list("start_time", "end_time")

        booked_slots = []
        for start, end in booked:
            booked_slots.append({"start": str(start), "end": str(end)})

        available_slots = []
        for schedule in schedules:
            current = schedule.start_time
            while current < schedule.end_time:
                slot_end = (
                    (
                        timezone.datetime.combine(date, current) + timedelta(minutes=30)
                    ).time()
                    if current
                    else None
                )
                if slot_end and slot_end <= schedule.end_time:
                    is_booked = any(b["start"] == str(current) for b in booked_slots)
                    if not is_booked:
                        available_slots.append(
                            {"start": str(current), "end": str(slot_end)}
                        )
                if current:
                    current = (
                        timezone.datetime.combine(date, current) + timedelta(minutes=30)
                    ).time()

        return Response({"available": True, "slots": available_slots})

    def create(self, request):
        serializer = AppointmentCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        try:
            physio = User.objects.get(id=data["physiotherapist_id"])
        except User.DoesNotExist:
            return Response({"detail": "Physiotherapist not found"}, status=404)

        appointment = Appointment.objects.create(
            patient=request.user,
            physiotherapist=physio,
            date=data["date"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            patient_notes=data.get("patient_notes", ""),
        )

        return Response(
            AppointmentSerializer(appointment).data, status=status.HTTP_201_CREATED
        )


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        action = self.action

        if action == "list":
            inbox = self.request.query_params.get("inbox")
            if inbox == "true":
                return Message.objects.filter(recipient=user).order_by("-created_at")
            sent = self.request.query_params.get("sent")
            if sent == "true":
                return Message.objects.filter(sender=user).order_by("-created_at")
            return Message.objects.filter(sender=user) | Message.objects.filter(
                recipient=user
            )

        return Message.objects.filter(sender=user) | Message.objects.filter(
            recipient=user
        )

    def create(self, request):
        from .serializers import MessageCreateSerializer

        serializer = MessageCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            recipient = User.objects.get(id=data["recipient_id"])
        except User.DoesNotExist:
            return Response({"detail": "Recipient not found"}, status=404)

        message = Message.objects.create(
            sender=request.user,
            recipient=recipient,
            subject=data["subject"],
            body=data["body"],
        )

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):
        message = self.get_object()
        if message.recipient == request.user:
            message.is_read = True
            message.save()
        return Response(MessageSerializer(message).data)

    @action(detail=False, methods=["get"])
    def unread_count(self, request):
        count = Message.objects.filter(recipient=request.user, is_read=False).count()
        return Response({"unread_count": count})
