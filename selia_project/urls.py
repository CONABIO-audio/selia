from django.conf.urls import url
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Autocomplete
    url("autocomplete/irekua/", include("irekua_database.autocomplete")),
    url("autocomplete/schemas/", include("irekua_schemas.autocomplete")),
    url("autocomplete/terms/", include("irekua_terms.autocomplete")),
    url("autocomplete/items/", include("irekua_items.autocomplete")),
    url("autocomplete/geo/", include("irekua_geo.autocomplete")),
    url("autocomplete/devices/", include("irekua_devices.autocomplete")),
    url("autocomplete/annotations/", include("irekua_annotations.autocomplete")),
    url("autocomplete/collections/", include("irekua_collections.autocomplete")),
    # Item Thumbnails
    url("thumbnails/", include(("irekua_thumbnails.urls", "irekua_thumbnails"))),
    # Home
    url("", include(("selia.urls", "selia"))),
    # User Home
    url("home/", include(("selia_user_home.urls", "selia_user_home"))),
    # Registration
    url("registration/", include("selia_registration.urls")),
    # About
    url("about/", include(("selia_about.urls", "selia_about"))),
    # Upload App
    url("upload/", include(("selia_uploader.urls", "selia_uploader"))),
    url("visualizer/", include(("selia_visualizers.urls", "selia_visualizers"))),
    url(r"^api/", include(("irekua_api_project.urls", "irekua_api_project"))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
