from django.urls import path
from . import views

urlpatterns = [
    path('add-project/', views.AddProjectView.as_view(), name='add_project'),
    path("", views.IndexView.as_view(), name="index"),    
]