from django.apps import AppConfig
from oscar.apps.checkout.apps import CheckoutConfig as CoreCheckoutConfig
from .views import NovaPoshtaWarehousesAPIView, NovaPoshtaCityAPIView
from django.urls import path


class CheckoutConfig(CoreCheckoutConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "checkout"

    def ready(self):
        super().ready()
        self.extra_view = NovaPoshtaWarehousesAPIView

    def get_urls(self):
        urls = super().get_urls()
        urls += [
            path(
                "api_nova_poshta_warehouses/<str:city>/",
                self.extra_view.as_view(),
                name="nova_poshta_warehouses",
            ),
        ]
        urls += [
            path(
                "api_nova_poshta_cities/",
                NovaPoshtaCityAPIView.as_view(),
                name="api_nova_poshta_cities",
            )
        ]

        return self.post_process_urls(urls)
