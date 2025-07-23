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

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ''}),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = '' 
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = '' 