from django.contrib import admin
from .models import Person, Webpage, Project

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(Webpage)
class WebpageAdmin(admin.ModelAdmin):
    list_display = ('url',)
    search_fields = ('url',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    search_fields = ('name',)
    list_filter = ('start_date', 'end_date')
    filter_horizontal = ('team_members', 'approvers', 'webpages')

    fieldsets = (
    (None, {
        'fields': ('name', 'description', 'start_date', 'end_date')
    }),
    ('People Involved', {
        'fields': ('team_members', 'approvers'),
    }),
    ('Project Webpages', {
        'fields': ('webpages',),
    }),
    ('PDF Links', {
        'fields': ('email_pdf_url', 'comparison_pdf_url'),
    }),
)


