from django.conf import settings
from django.db import models  # noqa
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _  # noqa
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from shared.models import BaseModel, BaseSafeDeleteModel
from .managers import UserManager, ExecutiveUserManager, TechnicalUserManager, AcademicUserManager

# Create your models here.

def user_picture_bucket(instance, filename):
    return f'{instance.email}/pictures/{filename}'

class User(AbstractBaseUser, PermissionsMixin, BaseModel):

    class Type(models.TextChoices):
        EXECUTIVE = 'executive', _("Executive")
        TECHNICAL = 'technical', _("Técnico")
        ACADEMIC = 'academic', _("Academic")

    name = models.CharField(max_length=100, verbose_name=_("nome completo"))
    email = models.EmailField(unique=True, verbose_name=_("email"))
    email_alternate = models.EmailField(blank=True, null=True, verbose_name=_("email alternativo"))
    document = models.CharField(unique=True, max_length=14, null=True, verbose_name=_("documento"))
    cellphone = models.CharField(max_length=16, null=True, verbose_name=_("celular"))
    phone = models.CharField(max_length=16, blank=True, null=True, verbose_name=_("telefone"))
    type = models.CharField(
        max_length=14,
        choices=Type.choices,
        default=Type.TECHNICAL,
        verbose_name=_("tipo")
    )
    is_brazilian = models.BooleanField(null=True, verbose_name=_("brasileiro?"))

    is_staff = models.BooleanField(
        default=False,
        verbose_name=_("staff status"),
        help_text=_('Designates whether the user can log into this admin site.')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("active"),
        help_text=_("Designates whether this user should be treated as active."
                    " Unselect this instead of deleting accounts.")
    )
    picture = models.ImageField(
        upload_to=user_picture_bucket,
        blank=True,
        null=True,
        verbose_name=_('profile picture')
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    @property
    def is_executive(self):
        return self.type == self.Type.EXECUTIVE

    @property
    def is_technical(self):
        return self.type == self.Type.TECHNICAL

    @property
    def is_academic(self):
        return self.type == self.Type.ACADEMIC

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        """
        Returns the first name for the user.
        """
        return self.name.split(' ')[0]

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        from_email = from_email or settings.DEFAULT_FROM_EMAIL
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def activate(self, commit=True):
        """
        Activate an user
        """
        if self.is_active is False:
            self.is_active = True
        if commit:
            self.save()

    def deactivate(self, commit=True):
        """
        Deactivate an user
        """
        if self.is_active:
            self.is_active = False
        if commit:
            self.save()


class ExecutiveUser(User):
    objects = ExecutiveUserManager()

    class Meta:
        proxy = True
        verbose_name = _("usuário executivo")
        verbose_name_plural = _("usuários executivos")


class TechnicalUser(User):
    objects = TechnicalUserManager()

    class Meta:
        proxy = True
        verbose_name = _("usuário técnico")
        verbose_name_plural = _("usuários técnicos")


class AcademicUser(User):
    objects = AcademicUserManager()

    class Meta:
        proxy = True
        verbose_name = _("usuário acadêmico")
        verbose_name_plural = _("usuários acadêmicos")


class TechnicalProfile(BaseSafeDeleteModel):
    user = models.OneToOneField(
        'TechnicalUser',
        on_delete=models.CASCADE,
        related_name='technical',
        verbose_name=_("usuário")
    )
    department = models.CharField(
        max_length=254,
        null=True, blank=True,
        verbose_name=_("departamento/Seção")
    )
    coordination = models.CharField(
        max_length=254,
        null=True, blank=True,
        verbose_name=_("coordenação/Gerência")
    )
    role = models.CharField(
        max_length=254,
        null=True,
        verbose_name=_("cargo/Função")
    )

    class Meta:
        verbose_name = _("perfil técnico")
        verbose_name_plural = _("perfis técnicos")

class ExecutiveProfile(BaseSafeDeleteModel):
    user = models.OneToOneField(
        ExecutiveUser,
        on_delete=models.CASCADE,
        related_name='executive',
        verbose_name=_("usuário")
    )
    company = models.CharField(
        max_length=254,
        null=True, blank=True,
        verbose_name=_("empresa")
    )
    role = models.CharField(
        max_length=254,
        null=True,
        verbose_name=_("cargo/Função")
    )
    
    class Meta:
        verbose_name = _("perfil executivo")
        verbose_name_plural = _("perfis executivos")

class AcademicProfile(BaseSafeDeleteModel):
    user = models.OneToOneField(
        AcademicUser,
        on_delete=models.CASCADE,
        related_name='academic',
        verbose_name=_("usuário")
    )
    university = models.CharField(
        max_length=254,
        null=True, blank=True,
        verbose_name=_("empresa")
    )
    role = models.CharField(
        max_length=254,
        null=True,
        verbose_name=_("cargo/Função")
    )

    class Meta:
        verbose_name = _("perfil acadêmico")
        verbose_name_plural = _("perfis acadêmicos")