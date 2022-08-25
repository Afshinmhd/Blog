from enum import Enum
from django.utils.translation import gettext as _


class Messages(Enum):
    INVALID_FORMAT = _('This format is not supported')
    IMAGE_SIZE = _("Image size should not be larger than 2MB")
    DATABASE_ERROR = _("Database not available.")