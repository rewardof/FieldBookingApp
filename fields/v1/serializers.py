from rest_framework import serializers

from base.v1.serializers import AddressSerializer
from fields.dataclasses import FootballFieldData, AddressData
from fields.models import FootballField
from fields.services import FootballFieldService
from file.v1.serializers import FileSerializer
from user.v1.serializers import UserMiniSerializer


class FootballFieldSerializer(serializers.ModelSerializer):
    """
    used to create and update football fields

    if admin is creating a field, he should be able to set the owner
    if owner is creating a field, owner should be set automatically
    """
    address = AddressSerializer()

    class Meta:
        model = FootballField
        fields = (
            'id',
            'name',
            'address',
            'contact_number',
            'contact_number2',
            'description',
            'hourly_price',
            'images',
            'width',
            'length',
            'owner',
            'is_active'
        )
        extra_kwargs = {
            'name': {'required': True, 'allow_null': False},
            'address': {'required': True, 'allow_null': False},
            'contact_number': {'required': True, 'allow_null': False},
            'hourly_price': {'required': True, 'allow_null': False},
            'width': {'required': True, 'allow_null': False},
            'length': {'required': True, 'allow_null': False},
            'owner': {'required': False, 'allow_null': True},
        }

    def validate(self, attrs):
        if self.instance:
            owner = attrs.get('owner')
            if owner and owner != self.instance.owner:
                raise serializers.ValidationError("Owner cannot be changed.")
        return attrs

    def create(self, validated_data):
        # Extract and create address data
        address_data = AddressData(**validated_data.pop('address'))

        # Create field data with address
        field_data = FootballFieldData(
            **validated_data,
            address_data=address_data
        )

        service = FootballFieldService()
        field = service.create_football_field(
            data=field_data,
            user=self.context['request'].user
        )

        return field

    def update(self, instance, validated_data):
        # Handle address update if provided
        AddressSerializer().update(instance.address, validated_data.pop('address'))

        # Handle images if provided
        if 'images' in validated_data:
            instance.images.clear()
            instance.images.set(validated_data.pop('images'))

        field = super().update(instance, validated_data)

        return field

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['owner'] = UserMiniSerializer(instance.owner).data
        data['images'] = FileSerializer(instance.images.all(), many=True).data
        return data


class FootballFieldListSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    images = FileSerializer(many=True)

    class Meta:
        model = FootballField
        fields = (
            'id',
            'name',
            'address',
            'contact_number',
            'contact_number2',
            'description',
            'hourly_price',
            'images',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['distance'] = round(getattr(instance, 'distance', 0), 2)
        return data


class FootballDetailSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    owner = UserMiniSerializer()
    images = FileSerializer(many=True)

    class Meta:
        model = FootballField
        fields = (
            'id',
            'name',
            'address',
            'contact_number',
            'contact_number2',
            'description',
            'hourly_price',
            'images',
            'width',
            'length',
            'owner',
            'is_active'
        )


class FootballFieldMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = FootballField
        fields = (
            'id',
            'name',
        )