from django.views import generic
from django.urls import reverse
from django.forms import formset_factory, modelformset_factory
from django import forms
from django.db.models import Count
import requests
from .forms import ProjectForm, PersonEmailForm, WebpageURLForm
from .models import Person, Project, Webpage

# Create your views here.
class IndexView(generic.ListView):
    template_name = "projectManager/index.html"
    context_object_name = "latest_project_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Project.objects.order_by("-end_date")[:5]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['top_contributors'] = (
            Person.objects
            .annotate(project_count=Count('projects_worked_on'))
            .filter(project_count__gt=0)
            .order_by('-project_count')[:5]
        )

        context['top_approvers'] = (
            Person.objects
            .annotate(approval_count=Count('projects_approved'))
            .filter(approval_count__gt=0)
            .order_by('-approval_count')[:5]
        )

        return context

class AllProjectsView(generic.ListView):
    template_name = "projectManager/projects.html"
    context_object_name = "project_list"

    def get_queryset(self):
        return Project.objects.order_by("-end_date")

class AboutDeveloperView(generic.TemplateView):
    template_name="projectManager/about.html"

class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = 'projectManager/project-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Check which webpages are reachable
        valid_pages = []
        for page in self.object.webpages.all():
            try:
                response = requests.head(page.url, timeout=5)
                if response.status_code == 200:
                    valid_pages.append(page)
            except requests.RequestException:
                pass  # Ignore unreachable pages

        context['valid_webpages'] = valid_pages
        return context
    
class AddProjectView(generic.FormView):
    template_name = 'projectManager/add-project.html'
    form_class = ProjectForm
    
    # Use modelformset_factory for your ModelForms
    team_member_formset_class = modelformset_factory(
        Person,
        form=PersonEmailForm,
        extra=0,
        min_num=1,
        validate_min=True,
        fields=['email'],
        widgets={'email': forms.EmailInput(attrs={'class': 'form-control'})}
    )

    approver_formset_class = modelformset_factory(
        Person,
        form=PersonEmailForm,
        extra=0,
        min_num=1,
        validate_min=True,
        fields=['email'],
        widgets={'email': forms.EmailInput(attrs={'class': 'form-control'})}
    )

    webpage_formset_class = modelformset_factory(
        Webpage,
        form=WebpageURLForm,
        extra=0,
        min_num=1,
        validate_min=True,
        fields=['url'],
        widgets={'url': forms.URLInput(attrs={'class': 'form-control'})}
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['team_member_formset'] = self.team_member_formset_class(self.request.POST, queryset=Person.objects.none(), prefix='team_members')
            context['approver_formset'] = self.approver_formset_class(self.request.POST, queryset=Person.objects.none(), prefix='approvers')
            context['webpage_formset'] = self.webpage_formset_class(self.request.POST, queryset=Webpage.objects.none(), prefix='webpages')
        else:
            context['team_member_formset'] = self.team_member_formset_class(queryset=Person.objects.none(), prefix='team_members')
            context['approver_formset'] = self.approver_formset_class(queryset=Person.objects.none(), prefix='approvers')
            context['webpage_formset'] = self.webpage_formset_class(queryset=Webpage.objects.none(), prefix='webpages')

        return context

    def form_valid(self, form):
        team_member_formset = self.team_member_formset_class(self.request.POST, prefix='team_members')
        approver_formset = self.approver_formset_class(self.request.POST, prefix='approvers')
        webpage_formset = self.webpage_formset_class(self.request.POST, prefix='webpages')

        if team_member_formset.is_valid() and approver_formset.is_valid() and webpage_formset.is_valid():
            data = form.cleaned_data
            project = Project.objects.create(
                name=data['name'],
                start_date=data['start_date'],
                end_date=data['end_date'],
                email_pdf_url=data['email_pdf_url'],
                comparison_pdf_url=data['comparison_pdf_url'],
            )

            for f in team_member_formset:
                if f.cleaned_data:
                    email = f.cleaned_data.get('email')
                    if email:
                        person, _ = Person.objects.get_or_create(email=email, defaults={'name': email.split('@')[0]})
                        project.team_members.add(person)

            for f in approver_formset:
                if f.cleaned_data:
                    email = f.cleaned_data.get('email')
                    if email:
                        person, _ = Person.objects.get_or_create(email=email, defaults={'name': email.split('@')[0]})
                        project.approvers.add(person)

            for f in webpage_formset:
                if f.cleaned_data:
                    url = f.cleaned_data.get('url')
                    if url:
                        webpage, _ = Webpage.objects.get_or_create(url=url)
                        project.webpages.add(webpage)

            # Redirect to the new project's detail page
            self.success_url = reverse('project_detail', kwargs={'pk': project.pk}) + '?success=1'
            return super().form_valid(form)
        else:
            context = self.get_context_data(form=form)
            context['team_member_formset'] = team_member_formset
            context['approver_formset'] = approver_formset
            context['webpage_formset'] = webpage_formset
            return self.render_to_response(context)