from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.db.transaction import atomic
from django.utils.translation import gettext_lazy as _

from apps.restauth.serializers import PasswordResetSerializer
from shared.fields import DocumentField, PhoneNumberField
from shared.validators import NamedBRCPFValidator
from .models import ExecutiveUser, TechnicalProfile, TechnicalUser, User

DUPLICATE_DOCUMENT = _("Já existe um usuário cadastrado com este documento.")


class TechnicalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalProfile
        fields = [
            'institution',
            'department',
            'coordination',
            'role',
        ]
        extra_kwargs = {
            'role': {'required': True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # TODO: add institution serializer here (not implemented yet).
        return data


class BaseUserSerializer(serializers.ModelSerializer):
    document = DocumentField(
        validators=[UniqueValidator(queryset=User.objects.all(), message=DUPLICATE_DOCUMENT)]
    )
    cellphone = PhoneNumberField()

    class Meta:
        model = User
        fields = [
            'id',
            'type',
            'email',
            'name',
            'document',
            'cellphone',
            'is_brazilian',
            'is_staff',
            'is_active',
            'picture',
        ]
        extra_kwargs = {
            'is_brazilian': {'required': True},
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True},
        }

    def validate(self, attrs):
        is_brazilian = attrs.get('is_brazilian')
        if is_brazilian:
            validator = NamedBRCPFValidator('document')
            validator(attrs['document'])
        return attrs


class ExecutiveUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = ExecutiveUser


class TechnicalUserSerializer(BaseUserSerializer):
    email_alternate = serializers.EmailField(required=False)
    phone = PhoneNumberField(required=False)
    technical = TechnicalProfileSerializer()

    class Meta(BaseUserSerializer.Meta):
        model = TechnicalUser
        fields = BaseUserSerializer.Meta.fields + [
            'email_alternate',
            'phone',
            'technical',
        ]

    @atomic
    def create(self, validated_data):
        profile_data = validated_data.pop('technical')
        profile_data['institution'] = profile_data['institution'].pk

        # Create user
        user = TechnicalUser.objects.create_user(**validated_data)

        # Create technical profile
        serializer = TechnicalProfileSerializer(data=profile_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)

        # Send reset password e-mail
        serializer = PasswordResetSerializer(data={'email': user.email}, context=self.context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return user