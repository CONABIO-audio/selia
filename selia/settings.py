from irekua_dev_settings.settings import *
from irekua_database.settings import *
from irekua_schemas.settings import *
from irekua_terms.settings import *
from irekua_geo.settings import *
from irekua_types.settings import *
from irekua_items.settings import *
from irekua_models.settings import *
from irekua_devices.settings import *
from irekua_organisms.settings import *
from irekua_annotators.settings import *
from irekua_visualizers.settings import *
from irekua_collections.settings import *
from irekua_annotations.settings import *
from irekua_thumbnails.settings import *
from irekua_upload.settings import *


LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

SELIA_APPS = (
    IREKUA_BASE_APPS +
    IREKUA_DATABASE_APPS +
    IREKUA_SCHEMAS_APPS +
    IREKUA_TERMS_APPS +
    IREKUA_TYPES_APPS +
    IREKUA_DEVICES_APPS +
    IREKUA_GEO_APPS +
    IREKUA_ITEMS_APPS +
    IREKUA_COLLECTIONS_APPS +
    IREKUA_ORGANISMS_APPS +
    IREKUA_MODELS_APPS +
    IREKUA_ANNOTATORS_APPS +
    IREKUA_VISUALIZERS_APPS +
    IREKUA_ANNOTATIONS_APPS +
    IREKUA_THUMBNAILS_APPS +
    IREKUA_UPLOAD_APPS +
    [
        'selia',
    ]
)

ITEM_DETAIL_APP = 'selia'
