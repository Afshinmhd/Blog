from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from common.basemodel import BaseModel
from .utils import image_path


class ArticleModel(BaseModel):
    """
        This class used to store articles
    """
    
    author = models.ForeignKey(User, verbose_name=_('author'), on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=60)
    body = models.TextField(_('body'))

    def __str__(self):
        return self.title


class ArticleImageModel(BaseModel):
    """
        This class used to store article images
    """
    
    article = models.ForeignKey(
        ArticleModel, verbose_name=_('article'), on_delete=models.CASCADE)

    image = models.ImageField(_('image'), upload_to=image_path, null=True, blank=True)

    def __str__(self):
        return self.image.name

