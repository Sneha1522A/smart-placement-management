from django import forms
from django.utils import timezone
from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title',
            'company',
            'location',
            'job_type',
            'package',
            'description',
            'min_cgpa',
            'eligible_branches',
            'deadline',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Software Engineer'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Acme Corp'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Bengaluru, KA'
            }),
            'job_type': forms.Select(attrs={
                'class': 'form-control form-select'
            }),
            'package': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 12 LPA (optional)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Detailed job description, responsibilities, and key skills...'
            }),
            'min_cgpa': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '10',
                'placeholder': 'e.g. 7.50'
            }),
            'eligible_branches': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. CSE, ECE, ISE'
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline and deadline < timezone.now().date():
            raise forms.ValidationError("Deadline cannot be in the past.")
        return deadline

    def clean_min_cgpa(self):
        min_cgpa = self.cleaned_data.get('min_cgpa')
        if min_cgpa is not None:
            if min_cgpa < 0 or min_cgpa > 10:
                raise forms.ValidationError("Minimum CGPA must be between 0.00 and 10.00.")
        return min_cgpa
