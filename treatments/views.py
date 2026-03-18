from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg
from django.contrib.auth.models import User
from .models import TreatmentPlan, TreatmentExercise, ExerciseSession, LevelProgression
from .serializers import (
    TreatmentPlanSerializer,
    TreatmentPlanCreateSerializer,
    TreatmentExerciseSerializer,
    ExerciseSessionSerializer,
    LevelProgressionSerializer,
    RecordSessionSerializer,
)
from exercises.models import Exercise


class TreatmentPlanViewSet(viewsets.ModelViewSet):
    queryset = TreatmentPlan.objects.all()
    serializer_class = TreatmentPlanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = TreatmentPlan.objects.select_related(
            "patient", "physiotherapist"
        ).all()

        if hasattr(user, "physiotherapist") and user.physiotherapist:
            pass
        else:
            queryset = queryset.filter(patient=user)

        patient_id = self.request.query_params.get("patient_id")
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == "true")
        return queryset

    def create(self, request):
        from .serializers import TreatmentPlanCreateSerializer

        serializer = TreatmentPlanCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            patient = User.objects.get(id=data["patient_id"])
        except User.DoesNotExist:
            return Response({"detail": "Patient not found"}, status=404)

        plan = TreatmentPlan.objects.create(
            patient=patient,
            physiotherapist=request.user,
            name=data["name"],
            description=data.get("description", ""),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            is_active=True,
        )

        return Response(
            TreatmentPlanSerializer(plan).data, status=status.HTTP_201_CREATED
        )

    def partial_update(self, request, pk=None):
        plan = self.get_object()

        if request.data.get("name"):
            plan.name = request.data["name"]
        if "description" in request.data:
            plan.description = request.data.get("description", "")
        if "start_date" in request.data:
            plan.start_date = request.data.get("start_date")
        if "end_date" in request.data:
            plan.end_date = request.data.get("end_date")
        if "is_active" in request.data:
            plan.is_active = request.data["is_active"]

        plan.save()
        return Response(TreatmentPlanSerializer(plan).data)

    @action(detail=True, methods=["post"])
    def add_exercise(self, request, pk=None):
        plan = self.get_object()
        exercise_id = request.data.get("exercise_id")
        level = request.data.get("level", 1)

        if not exercise_id:
            return Response(
                {"detail": "exercise_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            exercise = Exercise.objects.get(id=exercise_id, is_active=True)
        except Exercise.DoesNotExist:
            return Response(
                {"detail": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND
            )

        existing = TreatmentExercise.objects.filter(
            treatment_plan=plan, exercise_id=exercise_id
        ).first()
        if existing:
            return Response(
                {"detail": "Exercise already exists in this plan"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        treatment_exercise = TreatmentExercise.objects.create(
            treatment_plan=plan,
            exercise_id=exercise.id,
            exercise_name=exercise.name,
            assigned_level=int(level),
            current_level=int(level),
            notes=request.data.get("notes", ""),
        )

        serializer = TreatmentExerciseSerializer(treatment_exercise)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def exercises(self, request, pk=None):
        plan = self.get_object()
        exercises = plan.exercises.all()
        serializer = TreatmentExerciseSerializer(exercises, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        plan = self.get_object()
        plan.is_active = True
        plan.save()
        return Response(TreatmentPlanSerializer(plan).data)

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        plan = self.get_object()
        plan.is_active = False
        plan.save()
        return Response(TreatmentPlanSerializer(plan).data)


class TreatmentExerciseViewSet(viewsets.ModelViewSet):
    queryset = TreatmentExercise.objects.all()
    serializer_class = TreatmentExerciseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = TreatmentExercise.objects.select_related("treatment_plan").all()
        plan_id = self.request.query_params.get("plan_id")
        if plan_id:
            queryset = queryset.filter(treatment_plan_id=plan_id)
        return queryset

    @action(detail=True, methods=["get"])
    def sessions(self, request, pk=None):
        exercise = self.get_object()
        sessions = exercise.sessions.all().order_by("-session_date")
        serializer = ExerciseSessionSerializer(sessions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):
        exercise = self.get_object()
        sessions = exercise.sessions.all().order_by("session_date")

        history_data = []
        for session in sessions:
            history_data.append(
                {
                    "date": session.session_date,
                    "eva_before": session.eva_before,
                    "eva_after": session.eva_after,
                    "is_completed": session.is_completed,
                }
            )

        avg_eva = sessions.aggregate(Avg("eva_after"))

        return Response(
            {
                "sessions": history_data,
                "average_eva_after": avg_eva["eva_after__avg"],
                "total_sessions": sessions.count(),
            }
        )

    @action(detail=True, methods=["post"])
    def record_session(self, request, pk=None):
        exercise = self.get_object()
        serializer = RecordSessionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        treatment_exercise_id = validated_data.pop("treatment_exercise_id")

        if treatment_exercise_id != exercise.id:
            return Response(
                {"detail": "Treatment exercise ID mismatch"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session = ExerciseSession.objects.create(
            treatment_exercise=exercise,
            eva_before=validated_data.get("eva_before"),
            eva_after=validated_data.get("eva_after"),
            is_completed=validated_data.get("is_completed", False),
            completion_notes=validated_data.get("completion_notes", ""),
        )

        response_data = {
            "session": ExerciseSessionSerializer(session).data,
            "level_advancement": None,
        }

        if (
            validated_data.get("is_completed")
            and validated_data.get("eva_after") is not None
        ):
            if validated_data["eva_after"] <= 6:
                response_data["can_advance"] = True
                if exercise.current_level < 5:
                    response_data["level_advancement"] = {
                        "current_level": exercise.current_level,
                        "next_level": exercise.current_level + 1,
                        "message": "¡Puedes avanzar al siguiente nivel!",
                    }
            else:
                response_data["can_advance"] = False
                response_data["level_advancement"] = {
                    "current_level": exercise.current_level,
                    "message": "El dolor es demasiado alto (EVA > 6). No puedes avanzar de nivel.",
                }

        return Response(response_data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def advance_level(self, request, pk=None):
        exercise = self.get_object()

        if exercise.current_level >= 5:
            return Response(
                {"detail": "Already at maximum level"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        last_session = (
            exercise.sessions.filter(is_completed=True)
            .order_by("-session_date")
            .first()
        )

        if not last_session:
            return Response(
                {"detail": "No completed sessions found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if last_session.eva_after and last_session.eva_after > 6:
            return Response(
                {"detail": "Cannot advance: EVA > 6 in last session"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        old_level = exercise.current_level
        exercise.current_level += 1
        exercise.save()

        LevelProgression.objects.create(
            treatment_exercise=exercise,
            from_level=old_level,
            to_level=exercise.current_level,
            reason=request.data.get(
                "reason", "Progreso automático tras sesión completada con EVA ≤ 6"
            ),
        )

        return Response(TreatmentExerciseSerializer(exercise).data)


class ExerciseSessionViewSet(viewsets.ModelViewSet):
    queryset = ExerciseSession.objects.all()
    serializer_class = ExerciseSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ExerciseSession.objects.select_related("treatment_exercise").all()
        exercise_id = self.request.query_params.get("exercise_id")
        if exercise_id:
            queryset = queryset.filter(treatment_exercise_id=exercise_id)
        return queryset


class LevelProgressionViewSet(viewsets.ModelViewSet):
    queryset = LevelProgression.objects.all()
    serializer_class = LevelProgressionSerializer
    permission_classes = [IsAuthenticated]
