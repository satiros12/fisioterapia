from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .models import Patient, Physiotherapist
from .serializers import PatientSerializer, PhysiotherapistSerializer, UserSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.select_related("user").all()

    @action(detail=False, methods=["get"])
    def me(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            patient = request.user.patient
            serializer = self.get_serializer(patient)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response(
                {"detail": "Patient profile not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class PhysiotherapistViewSet(viewsets.ModelViewSet):
    queryset = Physiotherapist.objects.all()
    serializer_class = PhysiotherapistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Physiotherapist.objects.select_related("user").all()
