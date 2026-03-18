from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Patient, Physiotherapist


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = Patient
        fields = [
            "id",
            "user",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "age",
            "condition",
            "notes",
            "created_at",
        ]

    def create(self, validated_data):
        username = validated_data.pop("username")
        password = validated_data.pop("password", None)
        first_name = validated_data.pop("first_name", "")
        last_name = validated_data.pop("last_name", "")
        email = validated_data.pop("email", "")

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        patient = Patient.objects.create(user=user, **validated_data)
        return patient


class PhysiotherapistSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Physiotherapist
        fields = ["id", "user", "license_number", "created_at"]
