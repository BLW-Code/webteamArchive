from django.contrib.sitemaps import Sitemap
from .models import Project
from django.urls import reverse


class ProjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Project.objects.all()

    def lastmod(self, obj):
        return obj.end_date  # or any DateField relevant

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['index', 'about', 'all_projects', 'add_project']

    def location(self, item):
        return reverse(item)

sitemaps = {
    'static': StaticViewSitemap,
    'projects': ProjectSitemap,
}   