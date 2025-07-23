from django.db import models
from django.urls import reverse

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Webpage(models.Model):
    url = models.URLField(unique=True)

    def __str__(self):
        return self.url

class Project(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)


    team_members = models.ManyToManyField('Person', related_name='projects_worked_on')
    approvers = models.ManyToManyField('Person', related_name='projects_approved')
    webpages = models.ManyToManyField('Webpage', related_name='projects')

    email_pdf_url = models.URLField("Email PDF URL", blank=True, null=True)
    comparison_pdf_url = models.URLField("Comparison PDF URL", blank=True, null=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('project_detail', args=[str(self.id)]) 

