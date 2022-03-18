from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _  # noqa


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class ExecutiveUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('type', self.model.Type.EXECUTIVE)

        if extra_fields.get('type') != self.model.Type.EXECUTIVE:
            raise ValueError("Executive User must have type='Executive'.")

        return super()._create_user(email, password, **extra_fields)

    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.Type.EXECUTIVE)


class TechnicalUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('type', self.model.Type.TECHNICAL)

        if extra_fields.get('type') != self.model.Type.TECHNICAL:
            raise ValueError("Technical User must have type='technical'.")

        return super()._create_user(email, password, **extra_fields)

    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.Type.TECHNICAL)


class AcademicUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('type', self.model.Type.ACADEMIC)

        if extra_fields.get('type') != self.model.Type.ACADEMIC:
            raise ValueError("Academic User must have type='academic'.")

        return super()._create_user(email, password, **extra_fields)

    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.Type.ACADEMIC)
