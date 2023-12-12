from oscar.apps.checkout.forms import *
from django.utils.translation import gettext_lazy as _


class ShippingAddressForm(ShippingAddressForm):
    class Meta:
        model = get_model("order", "shippingaddress")
        fields = [
            "first_name",
            "last_name",
            "line4",
            "line1",
            # "state",
            # "postcode",
            "country",
            "phone_number",
            "notes",
        ]
        field_order = [
            "first_name",
            "last_name",
            "line4",
            "line1",
            "state",
            "country",
            "phone_number",
            "notes",
        ]

    line1 = forms.CharField(label=_("Branch number of Nova Poshta"))
