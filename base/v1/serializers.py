from rest_framework import serializers

from base.models import Address


class AddressSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='district.region.country.name', read_only=True)
    region = serializers.CharField(source='district.region.name', read_only=True)

    class Meta:
        model = Address
        fields = (
            'id',
            'country',
            'region',
            'district',
            'address_line',
            'zipcode',
            'latitude',
            'longitude',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['district'] = instance.district.name
        return data