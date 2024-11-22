from enum import Enum

from django.utils.translation import gettext_lazy as _


class Status(Enum):
    DRAFT = 'Draft'
    PUBLISHED = 'Published'
    ARCHIVED = 'Archived'


class Languages:
    ENGLISH = 'English'
    UZBEK = 'uzbek'
    RUSSIAN = 'russian'

    CHOICES = (
        (ENGLISH, _('English')),
        (UZBEK, _('Uzbek')),
        (RUSSIAN, _('Russian')),
    )


class UserTypes:
    CUSTOMER = 'customer'
    FIELD_OWNER = 'field_owner'
    ADMIN = 'admin'
    SUPER_ADMIN = 'super_admin'
    STAFFS = (ADMIN, FIELD_OWNER)

    CHOICES = (
        (CUSTOMER, _('Customer')),
        (ADMIN, _('Admin')),
        (FIELD_OWNER, _('Field Owner')),
    )
    LIST = [CUSTOMER, ADMIN, FIELD_OWNER]


class Gender:
    MALE = 'male'
    FEMALE = 'female'
    CHOICES = (
        (MALE, _("Male")),
        (FEMALE, _("Female"))
    )


class OrderStatus:
    CANCELLED = 'Cancelled'
    RECEIVED = 'Received'
    PREPARING = 'Preparing'
    ON_DELIVERY = 'On Delivery'
    DELIVERED = 'Delivered'

    CHOICES = (
        (CANCELLED, _("Cancelled")),
        (RECEIVED, _("Received")),
        (PREPARING, _("Preparing")),
        (ON_DELIVERY, _("On Delivery")),
        (DELIVERED, _("Delivered")),
    )


class PaymentMethod:
    VISA = 'visa'
    MASTERCARD = 'mastercard'
    PAYPAL = 'paypal'
    STRIPE = 'stripe'
    WALLET = 'wallet'
    CASH = 'cash'
    DEFAULT = STRIPE

    CHOICES = (
        (VISA, _(VISA)),
        (MASTERCARD, _(VISA)),
        (PAYPAL, _(PAYPAL)),
        (STRIPE, _(STRIPE)),
        (WALLET, _(WALLET)),
        (CASH, _(CASH))
    )


class AuthMethod:
    PHONE = 'phone'
    EMAIL = 'email'

    CHOICES = (
        (PHONE, _('Phone')),
        (EMAIL, _('Email')),
    )


class CodeType:
    REGISTER = 'register'
    LOGIN = 'login'
    FORGOT_PASSWORD = 'forgot_password'

    CHOICES = (
        (REGISTER, _('Register')),
        (LOGIN, _('Login')),
        (FORGOT_PASSWORD, _('Forgot Password')),
    )


class BookingStatus:
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'

    DEFAULT = PENDING

    CHOICES = (
        (PENDING, _("Pending")),
        (ACCEPTED, _("Accepted")),
        (REJECTED, _("Rejected")),
        (CANCELLED, _("Cancelled")),
        (COMPLETED, _("Completed")),
    )
