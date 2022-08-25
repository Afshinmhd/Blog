from django.db import models
from django.utils.translation import gettext as _


class BaseManager(models.Manager):
    
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False) 


class BaseModel(models.Model):
    """
        This class used to inheritance other models
    """

    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated_at'), auto_now=True)
    is_deleted = models.BooleanField(_('is deleted'), default=False)

    objects = BaseManager()

    class Meta:
        abstract = True