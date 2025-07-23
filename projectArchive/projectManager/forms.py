from django import forms
from .models import Project, Person, Webpage

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name',
            'start_date',
            'end_date',
            'description',
            'email_pdf_url',
            'comparison_pdf_url',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'email_pdf_url': forms.URLInput(attrs={'class': 'form-control'}),
            'comparison_pdf_url': forms.URLInput(attrs={'class': 'form-control'}),
        }

class PersonEmailForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'email': 'Email',
        }

class WebpageURLForm(forms.ModelForm):
    class Meta:
        model = Webpage
        fields = ['url']
        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'url': 'Webpage URL',
        }
