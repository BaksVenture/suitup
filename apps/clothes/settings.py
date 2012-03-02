import os
from django.conf import settings

DEFAULT_BRANDLOGO_PATH = os.path.join(settings.STATIC_URL, 'suitup', 'default_brand_logo.png')
DEFAULT_BRANDBACK_PATH = os.path.join(settings.STATIC_URL, 'suitup', 'default_brand_background.png')
DEFAULT_BRANDBORDER_PATH = os.path.join(settings.STATIC_URL, 'suitup', 'default_brand_border.png')
