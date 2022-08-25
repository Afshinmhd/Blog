from .messages import Messages
from django.conf import settings
from rest_framework.exceptions import ValidationError
from os import path
from django.utils import timezone


def is_image(ext):
    supported_ext = settings.SUPPORTED_IMAGE_FORMAT
    if ext.lower() not in supported_ext:
        raise ValidationError({'error': Messages.INVALID_FORMAT.value})
    return True


def image_path(instance, filename):
    ext = filename.split('.')[-1].lower()
    if is_image(ext):
        return path.join('.', 'images', '{}.{}'.format(int(timezone.now().timestamp()), ext))