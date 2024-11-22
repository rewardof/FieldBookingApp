from django.core.validators import MinValueValidator
from django.db import models

from bookings.models import Booking
from fields.managers import FootballFieldManager
from utils.validators import phone_number_validator


class FootballField(models.Model):
    """
    Model representing a football field with detailed information.
    """
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        help_text="The owner of this football field."
    )
    address = models.ForeignKey(
        "base.Address",
        on_delete=models.CASCADE,
        related_name="fields",
    )
    contact_number = models.CharField(
        max_length=15,
        help_text="Primary contact number for inquiries.",
        validators=[phone_number_validator()]
    )
    contact_number2 = models.CharField(
        max_length=15,
        blank=True,
        help_text="Secondary contact number (optional).",
        validators=[phone_number_validator()]
    )
    description = models.TextField(blank=True)
    hourly_price = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Hourly rental price for the field."
    )
    images = models.ManyToManyField(
        'file.File',
        related_name='fields',
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    width = models.SmallIntegerField(
        validators=[MinValueValidator(0)],
        help_text="Width of the field in meters."
    )
    length = models.SmallIntegerField(
        validators=[MinValueValidator(0)],
        help_text="Length of the field in meters."
    )
    objects = FootballFieldManager()

    def __str__(self):
        return self.name

    def is_booked_during(self, start_time, end_time):
        """
        Returns True if the field is booked for the given time slot.
        """
        return Booking.objects.filter(
            field=self,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status__in=['pending', 'accepted']
        ).exists()