from rest_framework import exceptions, serializers
from dj_rest_auth import serializers as dj_rest_auth_serializers
from dj_rest_auth.registration import serializers as dj_rest_auth_registration_serializers
from rest_framework.validators import UniqueValidator

from django.db.transaction import atomic
from django.utils.translation import gettext_lazy as _

from apps.user.models import ExecutiveUser, User
from shared.fields import DocumentField, PhoneNumberField
from shared.validators import NamedBRCPFValidator
from .forms import PasswordResetForm

DUPLICATE_DOCUMENT = _("Já existe um usuário cadastrado com este documento.")
DOCUMENT = 'document'


class PasswordResetSerializer(dj_rest_auth_serializers.PasswordResetSerializer):
    password_reset_form_class = PasswordResetForm


class LoginSerializer(dj_rest_auth_serializers.LoginSerializer):
    document = serializers.CharField(required=False)

    def _validate_document(self, document, password):
        user = None

        if document and password:
            user = self.authenticate(document=document, password=password)
        else:
            msg = _('Must include "document" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def get_auth_user(self, document, email, username, password):
        from allauth.account import app_settings

        if app_settings.AUTHENTICATION_METHOD == DOCUMENT:
            return self._validate_document(document, password)

        return super().get_auth_user(username, email, password)

    def validate(self, attrs):
        document = attrs.get('document')
        password = attrs.get('password')
        email = attrs.get('email')
        username = attrs.get('username')
        user = self.get_auth_user(document, email, username, password)

        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        self.validate_auth_user_status(user)

        attrs['user'] = user
        return attrs


class RegisterSerializer(dj_rest_auth_registration_serializers.RegisterSerializer):
    """Serializer to user self-register (only civil society members)."""
    name = serializers.CharField()
    email = serializers.EmailField()
    is_brazilian = serializers.BooleanField()
    document = DocumentField(
        validators=[UniqueValidator(queryset=User.objects.all(), message=DUPLICATE_DOCUMENT)]
    )
    cellphone = PhoneNumberField()

    def get_cleaned_data(self):
        return {
            'email': self.validated_data.get('email', ''),
            'password': self.validated_data.get('password1', ''),
            'name': self.validated_data['name'],
            'is_brazilian': self.validated_data['is_brazilian'],
            'document': self.validated_data['document'],
            'cellphone': self.validated_data['cellphone'],
        }

    def validate(self, attrs):
        if attrs['is_brazilian']:
            validator = NamedBRCPFValidator('document')
            validator(attrs['document'])
        return attrs

    @atomic
    def save(self, request):
        user = ExecutiveUser.objects.create_user(**self.get_cleaned_data())

        return user
