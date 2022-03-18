from localflavor.br.validators import BRCPFValidator

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class PhoneNumberValidator(RegexValidator):
    regex = r"(\+[0,9]{1,3})?([0-9]{2})?[0-9]?[0-9]{8}"
    message = _("Insira um número de telefone válido")
    code = 'invalid'


class NamedBRCPFValidator(BRCPFValidator):
    """
    A variation of locaflavor's BRCPFValidator that makes it
    possible to specify the field that triggered the error.
    """
    def __init__(self, field_name, *args, **kwargs):
        self.field_name = field_name
        super().__init__(*args, **kwargs)

    def __call__(self, value):
        try:
            super().__call__(value)
        except ValidationError as err:
            if self.field_name:
                raise ValidationError({self.field_name: err.message}, err.code)
            else:
                raise err
