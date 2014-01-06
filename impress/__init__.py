from django.conf import settings as django_settings
from os import path
import re


SLIDE_DELIMITER = re.compile(r'(?:\r?\n){3,}')


django_settings.configure(
    TEMPLATE_LOADERS=('django.template.loaders.filesystem.Loader',),
    TEMPLATE_DIRS=(path.abspath('./template'),)
)
