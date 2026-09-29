from django import forms
from .models import Company


class CompanyForm(forms.ModelForm):
    """
    Form for creating and editing company details.
    Includes custom widgets for styling and HTML5 date picker for deadline.
    """
    class Meta:
        model = Company
        fields = ['name', 'job_role', 'package_lpa', 'min_cgpa', 'deadline']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Google, Microsoft, Infosys',
                'required': True,
            }),
            'job_role': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Software Development Engineer',
                'required': True,
            }),
            'package_lpa': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'min': '0',
                'placeholder': 'e.g. 12.50',
                'required': True,
            }),
            'min_cgpa': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'min': '0.00',
                'max': '10.00',
                'placeholder': 'e.g. 7.50',
                'required': True,
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
                'required': True,
            }),
        }
