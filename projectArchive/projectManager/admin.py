from django.contrib import admin
from .models import Person, Webpage, Project

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')

@admin.register(Webpage)
class WebpageAdmin(admin.ModelAdmin):
    list_display = ('url',)
    search_fields = ('url',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    search_fields = ('name',)
    list_filter = ('start_date', 'end_date')
    filter_horizontal = ('workers', 'approvers', 'webpages')  # Makes multi-select UI cleaner
    fieldsets = (
        (None, {
            'fields': ('name', 'start_date', 'end_date')
        }),
        ('People Involved', {
            'fields': ('workers', 'approvers'),
        }),
        ('Project Webpages', {
            'fields': ('webpages',),
        }),
        ('Documents', {
            'fields': ('email_pdf', 'comparison_pdf'),
        }),
    )
