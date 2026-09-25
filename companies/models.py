from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="company_profile"
    )
    company_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(
        upload_to="company_logos/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.company_name
