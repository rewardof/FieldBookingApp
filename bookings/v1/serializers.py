from rest_framework import serializers

from bookings.dataclasses import BookingData
from bookings.models import Booking
from bookings.services import BookingService


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and displaying bookings.
    """
    field_name = serializers.CharField(source='field.name', read_only=True)
    hours = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = (
            'id',
            'field',
            'field_name',
            'start_time',
            'end_time',
            'total_price',
            'status',
            'hours'
        )
        extra_kwargs = {
            'end_time': {'read_only': True},
            'total_price': {'read_only': True},
            'status': {'read_only': True}
        }

    def create(self, validated_data):
        """
        Custom create method to use BookingService.
        """
        booking_data = BookingData(
            field=validated_data.get('field'),
            user=self.context['request'].user,
            start_time=validated_data.get('start_time'),
            hours=validated_data.get('hours')
        )

        return BookingService.process_booking(booking_data)
