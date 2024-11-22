from django.db import transaction

from base.models import Address
from fields.dataclasses import FootballFieldData, AddressData
from fields.models import FootballField
from fields.validators import FieldValidator
from user.models import User


class AddressCreator:
    """Separate class for address creation logic"""

    @staticmethod
    def create(data: AddressData) -> Address:
        return Address.objects.create(
            address_line=data.address_line,
            district=data.district,
            zipcode=data.zipcode,
            longitude=data.longitude,
            latitude=data.latitude
        )


class FootballFieldService:
    """
    Service class for handling football field operations.
    """

    @staticmethod
    @transaction.atomic
    def create_football_field(data: FootballFieldData, user: User) -> FootballField:
        validator = FieldValidator(data, user)
        validator.validate()

        if not data.owner:
            data.owner = user

        address = AddressCreator().create(data.address_data)

        field = FootballField.objects.create(
            name=data.name,
            address=address,
            contact_number=data.contact_number,
            contact_number2=data.contact_number2,
            description=data.description,
            hourly_price=data.hourly_price,
            width=data.width,
            length=data.length,
            owner=data.owner,
        )

        field.images.set(data.images)

        return field
