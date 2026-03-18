from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import (
    BodySegment,
    BodySubSegment,
    ExerciseCategory,
    Pathology,
    Muscle,
    Exercise,
)
from .serializers import (
    BodySegmentSerializer,
    BodySubSegmentSerializer,
    ExerciseCategorySerializer,
    PathologySerializer,
    MuscleSerializer,
    ExerciseSerializer,
    ExerciseListSerializer,
)


class BodySegmentViewSet(viewsets.ModelViewSet):
    queryset = BodySegment.objects.all()
    serializer_class = BodySegmentSerializer
    permission_classes = [IsAuthenticated]


class BodySubSegmentViewSet(viewsets.ModelViewSet):
    queryset = BodySubSegment.objects.all()
    serializer_class = BodySubSegmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = BodySubSegment.objects.select_related("segment").all()
        segment_id = self.request.query_params.get("segment_id")
        if segment_id:
            queryset = queryset.filter(segment_id=segment_id)
        return queryset


class ExerciseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExerciseCategory.objects.all()
    serializer_class = ExerciseCategorySerializer
    permission_classes = [IsAuthenticated]


class PathologyViewSet(viewsets.ModelViewSet):
    queryset = Pathology.objects.all()
    serializer_class = PathologySerializer
    permission_classes = [IsAuthenticated]


class MuscleViewSet(viewsets.ModelViewSet):
    queryset = Muscle.objects.all()
    serializer_class = MuscleSerializer
    permission_classes = [IsAuthenticated]


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.filter(is_active=True).select_related(
        "sub_segment", "sub_segment__segment", "category"
    )
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return ExerciseListSerializer
        return ExerciseSerializer

    def get_queryset(self):
        queryset = Exercise.objects.filter(is_active=True).select_related(
            "sub_segment", "sub_segment__segment", "category"
        )

        sub_segment_id = self.request.query_params.get("sub_segment_id")
        if sub_segment_id:
            queryset = queryset.filter(sub_segment_id=sub_segment_id)

        segment_id = self.request.query_params.get("segment_id")
        if segment_id:
            queryset = queryset.filter(sub_segment__segment_id=segment_id)

        category_id = self.request.query_params.get("category_id")
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        level = self.request.query_params.get("level")
        if level:
            queryset = queryset.filter(level=level)

        pathology_id = self.request.query_params.get("pathology_id")
        if pathology_id:
            queryset = queryset.filter(pathologies__id=pathology_id)

        return queryset

    @action(detail=False, methods=["get"])
    def by_segment(self, request):
        segment_id = request.query_params.get("segment_id")
        if not segment_id:
            return Response({"detail": "segment_id is required"}, status=400)

        exercises = self.get_queryset().filter(sub_segment__segment_id=segment_id)
        serializer = self.get_serializer(exercises, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def categories(self, request):
        sub_segment_id = request.query_params.get("sub_segment_id")
        if not sub_segment_id:
            return Response({"detail": "sub_segment_id is required"}, status=400)

        categories = ExerciseCategory.objects.filter(
            exercises__sub_segment_id=sub_segment_id
        ).distinct()
        serializer = ExerciseCategorySerializer(categories, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def levels(self, request):
        sub_segment_id = request.query_params.get("sub_segment_id")
        category_id = request.query_params.get("category_id")

        if not sub_segment_id:
            return Response({"detail": "sub_segment_id is required"}, status=400)

        queryset = self.get_queryset().filter(sub_segment_id=sub_segment_id)
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        levels = queryset.values_list("level", flat=True).distinct()
        return Response(sorted(levels))

    @action(detail=True, methods=["get"])
    def next_level(self, request, pk=None):
        exercise = self.get_object()
        current_level = exercise.level

        next_exercises = Exercise.objects.filter(
            sub_segment=exercise.sub_segment,
            category=exercise.category,
            level=current_level + 1,
            is_active=True,
        )

        if not next_exercises.exists():
            return Response({"has_next_level": False})

        serializer = ExerciseListSerializer(next_exercises, many=True)
        return Response({"has_next_level": True, "exercises": serializer.data})
