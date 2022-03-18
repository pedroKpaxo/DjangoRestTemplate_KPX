from rest_framework.serializers import CharField

from django.utils.translation import gettext_lazy as _

from .validators import PhoneNumberValidator


class DocumentField(CharField):
    def __init__(self, **kwargs):
        kwargs.setdefault('max_length', 14)
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return data.replace('.', '').replace('-', '')


class PhoneNumberField(CharField):
    default_error_messages = {
        'max_digits': _(
            "Certifique-se de que este campo não tenha mais de {max_digits} algarismos."
        )
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        validator = PhoneNumberValidator()
        self.validators.append(validator)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data = data.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        if len(data) > 16:  # Only checks length after cleaning it.
            self.fail('max_digits', max_digits=16)
        return data
