from . import sampling_events
from . import collection_sites
from . import items
from . import deployments
from . import collection_devices
from . import licences
from . import collection_users


urlpatterns = (
    sampling_events.urlpatterns
    + collection_sites.urlpatterns
    + items.urlpatterns
    + deployments.urlpatterns
    + collection_devices.urlpatterns
    + licences.urlpatterns
    + collection_users.urlpatterns
)
