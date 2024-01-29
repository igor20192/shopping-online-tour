from django.contrib import sitemaps
from catalogue.models import Product, Category


class ProductSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.date_updated


class CategorySitemap(sitemaps.Sitemap):
    priority = 0.5
    chagefreq = "daily"

    def items(self):
        return Category.objects.all()
