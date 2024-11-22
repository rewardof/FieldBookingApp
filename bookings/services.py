from datetime import timedelta

from django.db import transaction
from rest_framework.exceptions import ValidationError

from bookings.dataclasses import BookingData
from bookings.models import Booking
from bookings.validators import BookingValidator
from utils.constants import BookingStatus


class BookingService:
    """
    Service class for handling booking operations.
    """

    @staticmethod
    @transaction.atomic
    def process_booking(booking_data: BookingData) -> Booking:
        """
        Create a booking for a specific field, user, and start time.
        Returns:
            Created Booking instance
        """
        end_time = booking_data.start_time + timedelta(hours=booking_data.hours)
        booking_data.end_time = end_time
        total_price = booking_data.field.hourly_price * booking_data.hours

        validator = BookingValidator(booking=booking_data)
        validator.validate()

        booking = Booking.objects.create(
            field=booking_data.field,
            user=booking_data.user,
            start_time=booking_data.start_time,
            end_time=booking_data.end_time,
            total_price=total_price,
            status=BookingStatus.PENDING
        )

        return booking

    def change_booking_status(self, booking: Booking, new_status: str):
        """
        Change the status of a booking.
        """
        if not self._is_valid_status_transition(booking.status, new_status):
            raise ValidationError("Invalid status transition")

        booking.status = new_status
        booking.save()

    def _is_valid_status_transition(self, current_status: str, new_status: str):
        # implement as needed according to business rules
        return True