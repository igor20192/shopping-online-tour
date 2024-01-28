from django.contrib import sitemaps
from django.db.models.base import Model
from django.urls import reverse
from oscar.apps.catalogue.models import Product


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.date_updated
