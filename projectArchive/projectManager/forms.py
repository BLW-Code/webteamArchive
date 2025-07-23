from django import forms
from .models import Project

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

class PersonForm(forms.Form):
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="First Name"
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Last Name"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="Email"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

class WebpageURLForm(forms.Form):
    url = forms.URLField(
        widget=forms.URLInput(attrs={'class': 'form-control'}),
        label="Webpage URL"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
