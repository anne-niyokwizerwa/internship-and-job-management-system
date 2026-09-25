from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )
    student_id = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=20)
    university = models.CharField(max_length=150)
    program = models.CharField(max_length=150)
    year_of_study = models.PositiveIntegerField()
    skills = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to="student_profiles/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Document(models.Model):
    DOCUMENT_TYPES = [
        ("CV", "CV"),
        ("Certificate", "Certificate"),
        ("Cover Letter", "Cover Letter"),
        ("Other", "Other"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    document_type = models.CharField(
        max_length=30,
        choices=DOCUMENT_TYPES
    )

    file = models.FileField(upload_to="student_documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.document_type}"
