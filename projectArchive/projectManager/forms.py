from django import forms

class ProjectForm(forms.Form):
    name = forms.CharField(label="Project Name", max_length=200)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    email_pdf_url = forms.URLField(label="Email PDF URL", required=False)
    comparison_pdf_url = forms.URLField(label="Comparison PDF URL", required=False)

class PersonEmailForm(forms.Form):
    email = forms.EmailField(label="Email")

class WebpageURLForm(forms.Form):
    url = forms.URLField(label="Webpage URL")
