from django.conf.urls import url
from django.conf.urls import include
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static


urlpatterns = [
    url("", include(("selia.urls", "selia"))),
    url("admin/", admin.site.urls),
    url("thumnails/", include(("irekua_thumbnails.urls", "irekua_thumbnails"))),
    url("home/", include(("selia_user_home.urls", "selia_user_home"))),
    url("autocomplete/irekua/", include("irekua_database.autocomplete")),
    url("autocomplete/schemas/", include("irekua_schemas.autocomplete")),
    url("autocomplete/terms/", include("irekua_terms.autocomplete")),
    url("autocomplete/items/", include("irekua_items.autocomplete")),
    url("autocomplete/geo/", include("irekua_geo.autocomplete")),
    url("autocomplete/devices/", include("irekua_devices.autocomplete")),
    url("autocomplete/annotations/", include("irekua_annotations.autocomplete")),
    url("autocomplete/collections/", include("irekua_collections.autocomplete")),
    url("registration/", include("selia_registration.urls")),
    url("about/", include(("selia_about.urls", "selia_about"))),
    # url(r"^api/", include("irekua_rest_api.urls")),
    # url(
    #     r"^processes/thumbnails/",
    #     include(("selia_thumbnails.urls", "selia_thumbnails")),
    # ),
    # url(r"^upload/", include(("selia_uploader.urls", "selia_uploader"))),
    # url(r"^annotator/", include(("selia_annotator.urls", "selia_annotator"))),
    # url(r"^visualizers/", include(("selia_visualizers.urls", "selia_visualizers"))),
    # url(r"^managers/", include(("selia_managers.urls", "selia_managers"))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
