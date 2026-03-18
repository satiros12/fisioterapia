from django.db import models


class BodySegment(models.Model):
    name = models.CharField(max_length=100)
    name_es = models.CharField(max_length=100, verbose_name="Nombre en español")
    atlas_image = models.ImageField(upload_to="atlas/", blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Body Segment"
        verbose_name_plural = "Body Segments"

    def __str__(self):
        return self.name


class BodySubSegment(models.Model):
    segment = models.ForeignKey(
        BodySegment, on_delete=models.CASCADE, related_name="sub_segments"
    )
    name = models.CharField(max_length=100)
    name_es = models.CharField(max_length=100, verbose_name="Nombre en español")
    atlas_image = models.ImageField(upload_to="atlas/", blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Body Sub-Segment"
        verbose_name_plural = "Body Sub-Segments"

    def __str__(self):
        return f"{self.segment.name} - {self.name}"


class ExerciseCategory(models.Model):
    name = models.CharField(max_length=50)
    name_es = models.CharField(max_length=50, verbose_name="Nombre en español")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Exercise Category"
        verbose_name_plural = "Exercise Categories"

    def __str__(self):
        return self.name


class Pathology(models.Model):
    name = models.CharField(max_length=100)
    name_es = models.CharField(max_length=100, verbose_name="Nombre en español")
    description = models.TextField(blank=True)
    affected_segments = models.ManyToManyField(BodySegment, related_name="pathologies")

    class Meta:
        verbose_name = "Pathology"
        verbose_name_plural = "Pathologies"

    def __str__(self):
        return self.name


class Muscle(models.Model):
    name = models.CharField(max_length=100)
    name_es = models.CharField(max_length=100, verbose_name="Nombre en español")
    sub_segments = models.ManyToManyField(BodySubSegment, related_name="muscles")

    class Meta:
        verbose_name = "Muscle"
        verbose_name_plural = "Muscles"

    def __str__(self):
        return self.name


class Exercise(models.Model):
    LEVEL_CHOICES = [
        (1, "Nivel 1"),
        (2, "Nivel 2"),
        (3, "Nivel 3"),
        (4, "Nivel 4"),
        (5, "Nivel 5"),
    ]

    sub_segment = models.ForeignKey(
        BodySubSegment, on_delete=models.CASCADE, related_name="exercises"
    )
    category = models.ForeignKey(
        ExerciseCategory, on_delete=models.CASCADE, related_name="exercises"
    )
    level = models.PositiveIntegerField(choices=LEVEL_CHOICES, default=1)

    name = models.CharField(max_length=200)
    description = models.TextField()
    instructions = models.TextField()

    reference_image = models.ImageField(upload_to="exercises/", blank=True, null=True)
    muscle_image = models.ImageField(
        upload_to="exercises/muscles/", blank=True, null=True
    )

    pathologies = models.ManyToManyField(
        Pathology, related_name="exercises", blank=True
    )
    muscles = models.ManyToManyField(Muscle, related_name="exercises", blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["level", "category", "name"]

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"
