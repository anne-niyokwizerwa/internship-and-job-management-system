from django import forms

from .models import Student


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'student_id',
            'phone',
            'university',
            'program',
            'year_of_study',
            'skills',
            'bio',
            'profile_picture',
        ]
        labels = {
            'student_id': 'Student ID',
            'phone': 'Phone',
            'university': 'University',
            'program': 'Program',
            'year_of_study': 'Year of Study',
            'skills': 'Skills',
            'bio': 'Bio',
            'profile_picture': 'Profile Picture',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'skills': forms.Textarea(attrs={'rows': 4}),
        }
