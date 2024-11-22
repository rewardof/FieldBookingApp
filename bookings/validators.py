from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List

import pytz
from rest_framework.exceptions import ValidationError

from bookings.dataclasses import BookingData


class BookingValidationRule(ABC):
    """Abstract base class for booking validation rules"""

    @abstractmethod
    def validate(self, booking: BookingData) -> None:
        pass


class TimeSlotRule(BookingValidationRule):
    def validate(self, booking: BookingData) -> None:
        """Validate booking time slot availability and duration"""
        # Ensure booking starts in the future
        if booking.start_time <= datetime.now(pytz.utc):
            raise ValidationError("Booking must be for a future time")

        # Maximum booking duration (e.g., 3 hours)
        max_duration = timedelta(hours=3)
        if booking.end_time - booking.start_time > max_duration:
            raise ValidationError("Maximum booking duration is 3 hours")

        # Ensure start time is before end time
        if booking.start_time >= booking.end_time:
            raise ValidationError("Start time must be before end time")


class AvailabilityRule(BookingValidationRule):
    def validate(self, booking: BookingData) -> None:
        """Check field availability for the requested time slot"""
        if booking.field.is_booked_during(booking.start_time, booking.end_time):
            raise ValidationError("Field is already booked for the selected time slot")


class UserBookingLimitRule(BookingValidationRule):
    def validate(self, booking: BookingData) -> None:
        """Limit number of bookings per user"""
        # Example: Limit to 3 active future bookings per user
        active_bookings = booking.user.get_active_bookings()
        if len(active_bookings) >= 3:
            raise ValidationError("Maximum number of active bookings reached")


class BookingValidator:
    """Validator for football field bookings"""

    def __init__(
            self,
            booking: BookingData,
            validation_rules: List[BookingValidationRule] = None
    ):
        self.booking = booking
        self.field = booking.field
        self.user = booking.user

        # Default validation rules if none provided
        self.validation_rules = validation_rules or [
            TimeSlotRule(),
            AvailabilityRule(),
            UserBookingLimitRule()
        ]

    def validate(self) -> None:
        """Run all validation rules"""
        for rule in self.validation_rules:
            rule.validate(self.booking)

    def add_validation_rule(self, rule: BookingValidationRule) -> None:
        """Add a new validation rule"""
        self.validation_rules.append(rule)
