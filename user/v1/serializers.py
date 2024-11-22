from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from base.v1.serializers import AddressSerializer
from user.managers import UserUniqueIdentifierChecker
from user.models import User, VerificationCode
from utils.constants import AuthMethod, UserTypes, CodeType
from utils.exceptions import UserNotVerified, UserAlreadyExists
from utils.validators import phone_number_validator


class EmailPhoneBaseSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_null=True)
    phone_number = serializers.CharField(
        required=False, validators=[phone_number_validator(), ],
        allow_null=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.auth_method = None

    def validate(self, attrs):
        email = attrs.get('email')
        phone_number = attrs.get('phone_number')
        if not email and not phone_number:
            raise ValidationError("Email or phone number is required")

        username, auth_method = self._get_username(email=email, phone_number=phone_number)
        self.user = User.objects.filter(username=username).first()
        self.auth_method = auth_method

        return attrs

    @staticmethod
    def _get_username(email, phone_number):
        if email:
            return email, AuthMethod.EMAIL
        if phone_number:
            return phone_number, AuthMethod.PHONE
        return None


class SendOTPSerializer(EmailPhoneBaseSerializer):
    def create(self, validated_data):
        validated_data['auth_method'] = self.auth_method
        validated_data['user_type'] = UserTypes.CUSTOMER

        code_type = CodeType.REGISTER
        try:
            self.user = User.objects.create_user(**validated_data)
        except UserNotVerified:
            pass
        except UserAlreadyExists:
            code_type = CodeType.LOGIN

        VerificationCode.send_code(
            user=self.user, code_type=code_type
        )
        return self.user


class VerifyOTPSerializer(EmailPhoneBaseSerializer):
    code = serializers.IntegerField(
        required=True, allow_null=False,
        write_only=True
    )

    def validate(self, attrs):
        super().validate(attrs)
        code = attrs.get('code')

        code_type = CodeType.REGISTER
        if not self.user:
            raise ValidationError("User not found")
        if self.user.is_verified:
            code_type = CodeType.LOGIN

        VerificationCode.check_code(
            user=self.user, code=code,
            code_type=code_type
        )

        return attrs

    def save(self):
        self.user.verify()
        return self.user


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'phone_number',
            'language',
            'last_login',
            'address',
        )


class StaffUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'phone_number',
            'date_of_birth',
            'gender',
            'language',
            'last_login',
            'user_type',
            'password',
        )
        extra_kwargs = {
            'full_name': {'required': True, 'allow_null': False},
            'gender': {'required': True, 'allow_null': False},
            'date_of_birth': {'required': True, 'allow_null': False},
            'user_type': {'required': True, 'allow_null': False},
            'password': {'required': True, 'allow_null': False, 'write_only': True},
        }

    def validate(self, attrs):
        if attrs['user_type'] == 'CUSTOMER':
            raise serializers.ValidationError('You cannot create customer user')
        checker = UserUniqueIdentifierChecker(attrs['phone_number'])
        if checker.is_registered():
            raise serializers.ValidationError('User with this phone number already exist')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_staff_user(**validated_data)
        return user


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'phone_number',
        )


