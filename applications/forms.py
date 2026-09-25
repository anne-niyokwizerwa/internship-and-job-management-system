from django import forms

from opportunities.models import Opportunity

from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            "opportunity",
            "cover_letter",
            "cv",
        ]
        widgets = {
            "opportunity": forms.Select(),
            "cover_letter": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Write your cover letter...",
                }
            ),
            "cv": forms.ClearableFileInput(
                attrs={
                    "accept": ".pdf,.doc,.docx",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["opportunity"].queryset = (
            Opportunity.objects.filter(status=True)
        )