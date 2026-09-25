from django import forms

from .models import Opportunity


class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = [
            'title',
            'description',
            'opportunity_type',
            'location',
            'requirements',
            'deadline',
        ]
        labels = {
            'title': 'Title',
            'description': 'Description',
            'opportunity_type': 'Opportunity Type',
            'location': 'Location',
            'requirements': 'Requirements',
            'deadline': 'Deadline',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
