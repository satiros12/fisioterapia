from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from patients.models import Patient, Physiotherapist
from exercises.models import (
    BodySegment,
    BodySubSegment,
    ExerciseCategory,
    Pathology,
    Muscle,
    Exercise,
)
from treatments.models import TreatmentPlan, TreatmentExercise


class Command(BaseCommand):
    help = "Seeds the database with sample data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        User.objects.filter(username="patient1").delete()
        User.objects.filter(username="physio1").delete()

        patient_user = User.objects.create_user(
            username="patient1",
            password="test123456",
            first_name="Juan",
            last_name="Pérez",
            email="juan@example.com",
        )
        Patient.objects.create(user=patient_user, age=35, condition="Lumbago crónico")

        physio_user = User.objects.create_user(
            username="physio1",
            password="test123456",
            first_name="Dra.",
            last_name="Martínez",
            email="martinez@fisioterapia.com",
        )
        Physiotherapist.objects.create(user=physio_user, license_number="COL-12345")

        column_segment, _ = BodySegment.objects.get_or_create(
            name="Columna",
            name_es="Columna Vertebral",
            description="Ejercicios para la columna vertebral",
        )

        cervical, _ = BodySubSegment.objects.get_or_create(
            segment=column_segment,
            name="Cervical",
            name_es="Cuello / Cervical",
            description="Ejercicios para la zona cervical",
        )
        lumbar, _ = BodySubSegment.objects.get_or_create(
            segment=column_segment,
            name="Lumbar",
            name_es="Zona Lumbar",
            description="Ejercicios para la zona lumbar",
        )

        stretch_cat, _ = ExerciseCategory.objects.get_or_create(
            name="Stretching",
            name_es="Estiramientos",
            description="Ejercicios de estiramiento",
        )
        mobility_cat, _ = ExerciseCategory.objects.get_or_create(
            name="Mobility",
            name_es="Movilidad Activa",
            description="Ejercicios de movilidad",
        )
        strength_cat, _ = ExerciseCategory.objects.get_or_create(
            name="Strength",
            name_es="Fuerza",
            description="Ejercicios de fortalecimiento",
        )

        if not Exercise.objects.exists():
            Exercise.objects.create(
                sub_segment=cervical,
                category=stretch_cat,
                level=1,
                name="Flexión cervical",
                description="Ejercicio de flexión suave del cuello para aliviar tensión",
                instructions="1. Siéntate erguido\n2. Baja lentamente la barbilla hacia el pecho\n3. Mantén 10 segundos\n4. Regresa a la posición inicial\n5. Repite 5 veces",
            )
            Exercise.objects.create(
                sub_segment=cervical,
                category=stretch_cat,
                level=1,
                name="Rotación cervical",
                description="Rotación suave del cuello para mejorar movilidad",
                instructions="1. Gira lentamente la cabeza hacia la derecha\n2. Mantén 10 segundos\n3. Regresa al centro\n4. Gira hacia la izquierda\n5. Repite 5 veces cada lado",
            )
            Exercise.objects.create(
                sub_segment=cervical,
                category=mobility_cat,
                level=1,
                name="Movilidad cervical activa",
                description="Ejercicios combinados de movilidad cervical",
                instructions="1. Realiza círculos con la cabeza\n2. 5 círculos hacia la derecha\n3. 5 círculos hacia la izquierda\n4. Mantén los hombros relajados",
            )
            Exercise.objects.create(
                sub_segment=cervical,
                category=strength_cat,
                level=2,
                name="Fuerza isométrica cervical",
                description="Ejercicios de fortalecimiento isométrico",
                instructions="1. Coloca la mano en la frente\n2. Empuja la cabeza hacia adelante\n3. Mantén 5 segundos\n4. Repite 10 veces",
            )
            Exercise.objects.create(
                sub_segment=lumbar,
                category=stretch_cat,
                level=1,
                name="Estiramiento de flexión lumbar",
                description="Estiramiento suave de la zona lumbar",
                instructions="1. Acuéstate boca arriba\n2. Lleva las rodillas al pecho\n3. Mantén 20 segundos\n4. Repite 3 veces",
            )
            Exercise.objects.create(
                sub_segment=lumbar,
                category=mobility_cat,
                level=1,
                name="Gato-vaca",
                description="Ejercicio de movilidad lumbar",
                instructions="1. En posición de cuadrupedia\n2. Arquea la espalda hacia arriba (gato)\n3. Mantén 3 segundos\n4. Baja el vientre hacia el suelo (vaca)\n5. Repite 10 veces",
            )
            Exercise.objects.create(
                sub_segment=lumbar,
                category=strength_cat,
                level=1,
                name="Puente de pelvis",
                description="Fortalecimiento de musculatura lumbar baja",
                instructions="1. Acuéstate boca arriba\n2. Dobla las rodillas\n3. Eleva la pelvis\n4. Mantén 5 segundos\n5. Baja lentamente\n6. Repite 15 veces",
            )
            Exercise.objects.create(
                sub_segment=lumbar,
                category=strength_cat,
                level=2,
                name="Plancha lumbar",
                description="Fortalecimiento profundo",
                instructions="1. En posición de plancha\n2. Apoya antebrazos\n3. Mantén 30 segundos\n4. Descansa 15 segundos\n5. Repite 3 veces",
            )

        shoulder_segment, _ = BodySegment.objects.get_or_create(
            name="Hombro",
            name_es="Hombro / Articulación escapulohumeral",
            description="Ejercicios para el hombro",
        )

        if not BodySubSegment.objects.filter(segment=shoulder_segment).exists():
            shoulder_sub, _ = BodySubSegment.objects.get_or_create(
                segment=shoulder_segment,
                name="Hombro",
                name_es="Hombro",
                description="Ejercicios para el hombro",
            )
            Exercise.objects.create(
                sub_segment=shoulder_sub,
                category=stretch_cat,
                level=1,
                name="Estiramiento pectoral",
                description="Estiramiento de músculos pectorales",
                instructions="1. Párate en el marco de una puerta\n2. Coloca el antebrazo en el marco\n3. Gira el cuerpo hacia afuera\n4. Mantén 20 segundos\n5. Repite 3 veces",
            )

        if not TreatmentPlan.objects.exists():
            plan = TreatmentPlan.objects.create(
                patient=patient_user,
                physiotherapist=physio_user,
                name="Plan inicial - Cervical",
                description="Ejercicios para cervicalgia",
                is_active=True,
            )
            exercises = Exercise.objects.all()[:3]
            for ex in exercises:
                TreatmentExercise.objects.create(
                    treatment_plan=plan,
                    exercise_id=ex.id,
                    exercise_name=ex.name,
                    assigned_level=ex.level,
                    current_level=ex.level,
                )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
        self.stdout.write("Patient user: patient1 / test123456")
        self.stdout.write("Physio user: physio1 / test123456")
