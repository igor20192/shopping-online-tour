"""
URL configuration for shopping_online_tour project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from sitemaps import ProductSitemap, CategorySitemap


sitemaps = {"product": ProductSitemap, "category": CategorySitemap}


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("i18n/", include("django.conf.urls.i18n")),
        path("", include(apps.get_app_config("oscar").urls[0])),
        path(
            "sitemap.xml",
            sitemap,
            {"sitemaps": sitemaps},
            name="django.contrib.sitemaps.views.sitemap",
        ),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
