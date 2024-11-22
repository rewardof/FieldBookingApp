from abc import ABC, abstractmethod
from typing import List

from rest_framework.exceptions import ValidationError

from fields.dataclasses import FootballFieldData
from utils.constants import UserTypes


class ValidationRule(ABC):
    """Abstract base class for field validation rules"""

    @abstractmethod
    def validate(self, data: FootballFieldData, user) -> None:
        pass


class DimensionsRule(ValidationRule):
    def validate(self, data: FootballFieldData, user) -> None:
        if not (5 <= data.width <= 100):  # example dimensions
            raise ValidationError("Field width must be between 5 and 100 meters")

        if not (10 <= data.length <= 120):
            raise ValidationError("Field length must be between 10 and 120 meters")


class PriceRule(ValidationRule):
    def validate(self, data: FootballFieldData, user) -> None:
        if data.hourly_price <= 0:
            raise ValidationError("Hourly price must be positive")


class OwnerRule(ValidationRule):
    """Validates owner assignment based on user role"""

    def validate(self, data: FootballFieldData, user) -> None:
        if user.useer_type == UserTypes.ADMIN:
            if not data.owner:
                raise ValidationError(
                    "Owner field is required when creating field as admin"
                )


class FieldValidator:
    """Validator for football field creation/updates"""

    def __init__(
            self,
            data: FootballFieldData,
            user,
            validation_rules: List[ValidationRule] = None
    ):
        self.data = data
        self.user = user

        # Default validation rules if none provided
        self.validation_rules = validation_rules or [
            DimensionsRule(),
            PriceRule(),
        ]

    def validate(self) -> None:
        """Run all validation rules"""
        for rule in self.validation_rules:
            rule.validate(self.data, self.user)

    def add_validation_rule(self, rule: ValidationRule) -> None:
        """Add a new validation rule"""
        self.validation_rules.append(rule)
