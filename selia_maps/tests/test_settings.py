import os
from collections import OrderedDict

from irekua_dev_settings.settings import *
from irekua_database.settings import *


INSTALLED_APPS = list(OrderedDict.fromkeys(
    IREKUA_DATABASE_APPS +
    IREKUA_BASE_APPS
))
