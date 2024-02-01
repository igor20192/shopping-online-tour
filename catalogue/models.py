from django.db import models
from oscar.apps.catalogue.abstract_models import AbstractCategory, AbstractProduct
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy


class Category(AbstractCategory):
    keywords = models.TextField(_("keywords"), blank=True)


class Product(AbstractProduct):
    title = models.CharField(
        pgettext_lazy("Product title", "Title"), max_length=355, blank=True
    )
    keywords = models.TextField(_("keywords"), blank=True)


from oscar.apps.catalogue.models import *
