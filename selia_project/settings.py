import os
from collections import OrderedDict

from irekua_dev_settings.settings import *
from selia_templates.settings import *
from selia_registration.settings import *
from selia_about.settings import *
from selia_maps.settings import *
from selia.settings import *
from selia_user_home.settings import *
from selia_uploader.settings import *


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]


MIGRATION_MODULES = {
    "irekua_database": None,
    "irekua_schemas": None,
    "irekua_items": None,
    "irekua_terms": None,
    "irekua_upload": None,
    "irekua_geo": None,
    "irekua_models": None,
    "irekua_devices": None,
    "irekua_organisms": None,
    "irekua_annotators": None,
    "irekua_visualizers": None,
    "irekua_collections": None,
    "irekua_annotations": None,
    "irekua_thumbnails": None,
    "irekua_types": None,
}


INSTALLED_APPS = list(
    OrderedDict.fromkeys(
        IREKUA_BASE_APPS
        + SELIA_MAPS_APPS
        + SELIA_UPLOADER_APPS
        + SELIA_APPS
        + SELIA_USER_HOME_APPS
        + SELIA_ABOUT_APPS
        + SELIA_REGISTRATION_APPS
        + SELIA_TEMPLATES_APPS
    )
)

ROOT_URLCONF = "selia_project.urls"
