from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name} <{self.email}>"

class Webpage(models.Model):
    url = models.URLField(unique=True)

    def __str__(self):
        return self.url

class Project(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()

    workers = models.ManyToManyField(Person, related_name='projects_worked_on')
    approvers = models.ManyToManyField(Person, related_name='projects_approved')
    webpages = models.ManyToManyField(Webpage, related_name='projects')

    email_pdf = models.FileField(upload_to='project_pdfs/email_pdfs/')
    comparison_pdf = models.FileField(upload_to='project_pdfs/comparison_pdfs/')

    def __str__(self):
        return self.name
