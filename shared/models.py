from model_utils.fields import AutoCreatedField, AutoLastModifiedField
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    """
    Add timestamp control to a model.
    """
    created_at = AutoCreatedField(_('criado em'))
    updated_at = AutoLastModifiedField(_('modificado em'))

    class Meta:
        abstract = True


class BaseModel(TimeStampedMixin, models.Model):
    """
    An abstract base class model with timestamp control added.
    """
    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        # Allow uploaded files to be added during model creation.
        # This should be useful if the file field path uses instance's id.
        if self.id is None:
            saved = []
            for f in self.__class__._meta.get_fields():
                if isinstance(f, models.FileField):
                    saved.append((f.name, getattr(self, f.name)))
                    setattr(self, f.name, None)

            super().save(*args, **kwargs)

            for name, val in saved:
                setattr(self, name, val)

            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')
        super().save(*args, **kwargs)


class BaseSafeDeleteModel(BaseModel, SafeDeleteModel):
    """
    An abstract base class model that provides both timestamp
    and safe delete functionality.
    """
    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        abstract = True


class GeoSafeDeleteModel(TimeStampedMixin,SafeDeleteModel):

    _safedelete_policy = SOFT_DELETE_CASCADE
    class Meta:
        abstract = True
