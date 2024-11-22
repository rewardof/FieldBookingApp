from rest_framework.exceptions import ValidationError

from user.models import User


def send_confirmation_sms(user: User, code: int):
    """
    Send confirmation code to the user's phone number
    """
    body = f'Welcome to Field Booking Service App! Your confirmation code is {code}'
    send_sms(to=user.phone_number, body=body)


def send_sms(to, body):
    try:
        # here we should implement sms sending logic
        return
    except Exception as e:
        raise ValidationError(
            {'message': f'While sending sms we detected that there is an error. {e}'}
        )
