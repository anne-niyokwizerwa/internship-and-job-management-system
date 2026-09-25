from django.db import models
from companies.models import Company


class Opportunity(models.Model):
    OPPORTUNITY_TYPES = [
        ("Internship", "Internship"),
        ("Job", "Job"),
    ]

    CATEGORIES = [
        ("IT", "Information Technology"),
        ("Business", "Business"),
        ("Finance", "Finance"),
        ("Marketing", "Marketing"),
        ("Engineering", "Engineering"),
        ("Other", "Other"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="opportunities",
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    opportunity_type = models.CharField(
        max_length=20,
        choices=OPPORTUNITY_TYPES,
    )
    category = models.CharField(
        max_length=30,
        choices=CATEGORIES,
        default="Other",
    )
    location = models.CharField(max_length=150)
    requirements = models.TextField()
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title