from django.conf.urls import url
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(
        r'',
        include(('selia.urls', 'selia'))),
    url(
        r'^autocomplete/',
        include(('irekua_autocomplete.urls', 'irekua_autocomplete'))),
    url(
        r'^api/',
        include('irekua_rest_api.urls')),
    url(
        r'^registration/',
        include(('selia_registration.urls', 'selia_registration'))),
    url(
        r'^about/',
        include(('selia_about.urls', 'selia_about'))),
    url(
        r'^processes/thumbnails/',
        include(('selia_thumbnails.urls', 'selia_thumbnails'))),
    url(
        r'^upload/',
        include(('selia_uploader.urls', 'selia_uploader'))),
    url(
        r'^admin/',
        include(('selia_admin.urls', 'selia_admin'))),
    url(
        r'^annotator/',
        include(('selia_annotator.urls', 'selia_annotator'))),
    url(
        r'^visualizers/',
        include(('selia_visualizers.urls', 'selia_visualizers'))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
