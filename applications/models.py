from django.core.validators import FileExtensionValidator
from django.db import models

from students.models import Student
from opportunities.models import Opportunity


class Application(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="applications",
    )

    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE,
        related_name="applications",
    )

    cover_letter = models.TextField()

    cv = models.FileField(
        upload_to="cvs/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["pdf", "doc", "docx"],
            ),
        ],
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending",
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "opportunity")
        ordering = ["-applied_at"]

    def __str__(self):
        return f"{self.student} - {self.opportunity}"