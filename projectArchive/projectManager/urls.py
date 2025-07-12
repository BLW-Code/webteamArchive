from django.urls import path
from . import views

urlpatterns = [
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('add-project/', views.AddProjectView.as_view(), name='add_project'),
    path('projects/', views.AllProjectsView.as_view(), name='all_projects'),
    path("", views.IndexView.as_view(), name="index"),    
]