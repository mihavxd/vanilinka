from django.contrib.sitemaps import Sitemap
from .models import Category
from django.shortcuts import reverse

class StaticViewsSitemap(Sitemap):
    def items(self):
        return ['']
    def location(self, item):
        return item

class DynamicViewsSitemap(Sitemap):
    def items(self):
        return Category.objects.all()