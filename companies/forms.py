from django import forms
from .models import Company


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            "company_name",
            "phone",
            "email",
            "address",
            "website",
            "description",
            "logo",
        ]