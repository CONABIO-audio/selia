import os
from collections import OrderedDict

from irekua_dev_settings.settings import *
from irekua_database.settings import *
from irekua_models.settings import *
from irekua_rest_api.settings import *
from irekua_autocomplete.settings import *
from selia_templates.settings import *
from selia_registration.settings import *
from selia_about.settings import *
from selia_thumbnails.settings import *
from selia_uploader.settings import *
from selia_annotator.settings import *
from selia_visualizers.settings import *
from selia_maps.settings import *
from selia_managers.settings import *
from selia.settings import *


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale'), ]


INSTALLED_APPS = list(OrderedDict.fromkeys(
    SELIA_APPS +
    SELIA_MANAGERS_APPS +
    SELIA_MAPS_APPS +
    SELIA_VISUALIZERS_APPS +
    SELIA_ANNOTATOR_APPS +
    SELIA_UPLOADER_APPS +
    SELIA_THUMBNAILS_APPS +
    SELIA_ABOUT_APPS +
    SELIA_REGISTRATION_APPS +
    SELIA_TEMPLATES_APPS +
    IREKUA_AUTOCOMPLETE_APPS +
    IREKUA_REST_API_APPS +
    IREKUA_MODELS_APPS +
    IREKUA_DATABASE_APPS +
    IREKUA_BASE_APPS
))
