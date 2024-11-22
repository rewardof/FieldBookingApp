from django.db import models
from rest_framework.exceptions import ValidationError

from base.models import BaseModel
from utils.constants import BookingStatus


class Booking(BaseModel):
    """
    Represents a booking for a football field, including user, field, time slot, and status.
    """
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        help_text="The user who made the booking."
    )
    field = models.ForeignKey(
        'fields.FootballField',
        on_delete=models.CASCADE,
        help_text="The football field being booked."
    )
    start_time = models.DateTimeField(
        help_text="The start time of the booking."
    )
    end_time = models.DateTimeField(
        help_text="The end time of the booking."
    )
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.CHOICES,
        default=BookingStatus.PENDING,
        help_text="The current status of the booking."
    )
    total_price = models.IntegerField(
        help_text="The total price of the booking."
    )

    def clean(self):
        """
        Validates the booking to ensure the time slot does not overlap with existing bookings
        for the same field that are either pending or confirmed.
        """
        overlapping_bookings = Booking.objects.filter(
            field=self.field,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
            status__in=[BookingStatus.PENDING, BookingStatus.ACCEPTED]
        ).exclude(pk=self.pk)

        if overlapping_bookings.exists():
            raise ValidationError(
                "The selected time slot overlaps with an existing booking."
            )

    def save(self, *args, **kwargs):
        """
        Validates the booking before saving to ensure data integrity.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('field', 'start_time', 'end_time')
        ordering = ['-start_time']

