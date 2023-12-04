from django.apps import AppConfig
from oscar.apps.checkout.apps import *


class CheckoutConfig(CheckoutConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "checkout"
