from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import sitemaps

urlpatterns = [
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('about/', views.AboutDeveloperView.as_view(), name="about"),
    path('add-project/', views.AddProjectView.as_view(), name='add_project'),
    path('projects/', views.AllProjectsView.as_view(), name='all_projects'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path("", views.IndexView.as_view(), name="index"),    
]