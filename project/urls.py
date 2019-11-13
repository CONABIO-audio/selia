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
        include(('irekua_rest_api.urls', 'irekua_rest_api'))),
    url(
        r'^registration/',
        include(('selia_registration.urls', 'selia_registration'))),
    url(
        r'^about/',
        include(('selia_about.urls', 'selia_about')))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
