from oscar.apps.checkout.mixins import *
from oscar.apps.checkout.mixins import OrderPlacementMixin as CoreOrderPlacementMixin
from twilio.rest import Client
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class OrderPlacementMixin(CoreOrderPlacementMixin):
    """
    Custom OrderPlacementMixin for handling order placement with additional SMS notification functionality.

    This mixin extends the core OrderPlacementMixin from Django Oscar to include the ability to send an SMS
    notification when an order is successfully placed.

    Attributes:
        None

    Methods:
        send_sms_notification(order): Sends an SMS notification for a successfully placed order.
        handle_successful_order(order): Overrides the core method to include sending an SMS notification.
    """

    def send_sms_notification(self, order):
        """
        Send an SMS notification for a successfully placed order.

        Args:
            order (Order): The Order instance.

        Returns:
            None
        """
        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

            user_phone_number = settings.TO_PHONE_NUMBER

            message = client.messages.create(
                to=user_phone_number,
                from_=settings.TWILIO_PHONE_NUMBER,
                body=f"New order #{order.number} has been successfully placed",
            )

            logger.info(f"SMS successfully sent with SID: {message.sid}")
        except Exception as e:
            logger.error(f"Error sending SMS: {e}")

    def handle_successful_order(self, order):
        """
        Handle additional steps after an order has been successfully placed.

        Overrides the core method to include sending an SMS notification.

        Args:
            order (Order): The Order instance.

        Returns:
            HttpResponse: The HTTP response after handling the successful order.
        """
        response = super().handle_successful_order(order)
        self.send_sms_notification(order)

        return response
