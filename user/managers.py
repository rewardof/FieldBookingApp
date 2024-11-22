import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from utils.constants import AuthMethod, UserTypes
from utils.exceptions import UserNotVerified, UserAlreadyExists


class BaseUserQuerySet(QuerySet):
    """Custom queryset for models"""

    def hard_delete(self):
        super().delete()

    def delete(self):
        self.update(is_active=False)


class UserManager(BaseUserManager):
    def _create_user(self, username, email=None, phone_number=None, password=None,
                     user_type=None, auth_method=None, **extra_fields):
        if not username:
            raise ValueError(_('The given username must be set'))
        if not auth_method:
            raise ValueError(_('Auth method must be set'))

        checker = UserUniqueIdentifierChecker(email, username, auth_method=auth_method)
        if not checker.is_unique_username():
            if not checker.is_verified:
                raise UserNotVerified
            else:
                raise UserAlreadyExists(_(f"User with username: {username} already exists"))

        if email:
            email = self.normalize_email(email).lower()

        user = self.model(
            username=username.lower(), email=email,
            user_type=user_type, auth_method=auth_method,
            phone_number=phone_number, **extra_fields
        )
        if password:
            user.set_password(password)

        user.is_active = extra_fields.get('is_active', True)
        user.is_verified = self._get_is_verified(user_type)
        user.save(using=self._db)

        self._add_group(user, user_type)
        return user

    def create_user(self, username=None, email=None, phone_number=None, password=None,
                    user_type=None, auth_method=None, **extra_fields):
        if not username:
            username = self._determine_username(email, phone_number, auth_method)

        return self._create_user(
            username=username, email=email, phone_number=phone_number,
            password=password, user_type=user_type,
            auth_method=auth_method, **extra_fields
        )

    def _determine_username(self, email: str, phone_number: str, auth_method: str) -> str:
        if auth_method == AuthMethod.EMAIL:
            return email or str(uuid.uuid4())
        elif auth_method == AuthMethod.PHONE:
            return phone_number or str(uuid.uuid4())
        else:
            raise ValidationError("Auth method must be set")

    def create_superuser(self, username, email=None, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        user = self._create_user(
            username, email, phone_number, password,
            user_type=UserTypes.SUPER_ADMIN,
            auth_method=AuthMethod.EMAIL,
            **extra_fields
        )
        return user

    def _add_group(self, user: 'User', group_name: str):
        from django.contrib.auth.models import Group
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
        return user

    def _get_is_verified(self, user_type: str):
        if user_type != UserTypes.CUSTOMER:
            return True
        return False

    def _get_base_queryset(self):
        return super(UserManager, self).get_queryset()

    def get_queryset(self):
        """
        Return NOT DELETED objects.
        """
        return self._get_base_queryset().filter(is_active=True)

    def deleted(self):
        """
        Return DELETED objects.
        """
        return self._get_base_queryset().filter(is_active=False)

    def with_deleted(self):
        """
        Return ALL objects.
        """
        return self._get_base_queryset()


class UserUniqueIdentifierChecker:
    def __init__(self, email: str, phone_number: str,
                 user_type: str = None, auth_method: str = None):
        """
        :param user_type: CONSTANTS.UserType.CHOICES
        """
        self.email = email
        self.phone_number = phone_number
        self.user_type = user_type
        self.auth_method = auth_method
        self.username = self._get_username()
        self.user = get_user_model().objects.filter(username=self.username).first()
        self.is_verified = self.user.is_verified if self.user else None

    def is_email_unique(self):
        return not get_user_model().objects.filter(email=self.email).exists()

    def is_phone_unique(self):
        return not get_user_model().objects.filter(phone_number=self.phone_number).exists()

    def is_email_and_phone_unique(self):
        return self.is_email_unique() and self.is_phone_unique()

    def is_unique_username(self):
        return not self.user

    def _get_username(self):
        if self.auth_method == AuthMethod.EMAIL:
            username = self.email
        elif self.auth_method == AuthMethod.PHONE:
            username = self.phone_number
        else:
            username = self.email or self.phone_number
        return username
