from collections import OrderedDict

from irekua_database.settings import *
from irekua_geo.settings import *
from irekua_items.settings import *
from irekua_devices.settings import *
from irekua_collections.settings import *
from selia_templates.settings import *


SELIA_USER_HOME_APPS = list(
    OrderedDict.fromkeys(
        IREKUA_DATABASE_APPS
        + IREKUA_COLLECTIONS_APPS
        + IREKUA_DEVICES_APPS
        + IREKUA_ITEMS_APPS
        + IREKUA_DEVICES_APPS
        + [
            "selia_user_home",
        ]
        + SELIA_TEMPLATES_APPS
    )
)
