from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.forms import formset_factory
from .forms import ProjectForm, PersonEmailForm, WebpageURLForm
from .models import Person, Project, Webpage

# Create your views here.
class IndexView(generic.ListView):
    template_name = "projectManager/index.html"
    context_object_name = "latest_project_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Project.objects.order_by("-end_date")[:5]

class AllProjectsView(generic.ListView):
    template_name = "projectManager/projects.html"
    context_object_name = "project_list"

    def get_queryset(self):
        return Project.objects.order_by("-end_date")

class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = 'projectManager/project-detail.html'
    context_object_name = 'project'
    
class AddProjectView(generic.FormView):
    template_name = 'projectManager/add-project.html'
    form_class = ProjectForm
    success_url = reverse_lazy('project_success') 

    # Formset classes with team_members instead of workers
    team_member_formset_class = formset_factory(
        PersonEmailForm,
        extra=0,
        min_num=1,
        validate_min=True
    )
    approver_formset_class = formset_factory(
        PersonEmailForm,
        extra=0,
        min_num=1,
        validate_min=True
    )
    webpage_formset_class = formset_factory(
        WebpageURLForm,
        extra=0,
        min_num=1,
        validate_min=True
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['team_member_formset'] = self.team_member_formset_class(self.request.POST, prefix='team_members')
            context['approver_formset'] = self.approver_formset_class(self.request.POST, prefix='approvers')
            context['webpage_formset'] = self.webpage_formset_class(self.request.POST, prefix='webpages')
        else:
            context['team_member_formset'] = self.team_member_formset_class(prefix='team_members')
            context['approver_formset'] = self.approver_formset_class(prefix='approvers')
            context['webpage_formset'] = self.webpage_formset_class(prefix='webpages')

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
                        person, _ = Person.objects.get_or_create(
                            email=email,
                            defaults={'name': email.split('@')[0]}
                        )
                        project.team_members.add(person)  # Change 'workers' here if you renamed the field in your model

            for f in approver_formset:
                if f.cleaned_data:
                    email = f.cleaned_data.get('email')
                    if email:
                        person, _ = Person.objects.get_or_create(
                            email=email,
                            defaults={'name': email.split('@')[0]}
                        )
                        project.approvers.add(person)

            for f in webpage_formset:
                if f.cleaned_data:
                    url = f.cleaned_data.get('url')
                    if url:
                        webpage, _ = Webpage.objects.get_or_create(url=url)
                        project.webpages.add(webpage)

            return super().form_valid(form)
        else:
            context = self.get_context_data(form=form)
            context['team_member_formset'] = team_member_formset
            context['approver_formset'] = approver_formset
            context['webpage_formset'] = webpage_formset
            return self.render_to_response(context)