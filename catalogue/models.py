from django.db import models
from oscar.apps.catalogue.abstract_models import AbstractCategory, AbstractProduct
from django.utils.translation import gettext_lazy as _


class Category(AbstractCategory):
    keywords = models.TextField(_("keywords"), blank=True)


class Product(AbstractProduct):
    keywords = models.TextField(_("keywords"), blank=True)


from oscar.apps.catalogue.models import *
