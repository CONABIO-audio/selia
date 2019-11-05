from django.urls import path

from . import selia
from . import annotator

from . import create_views
from . import detail_views
from . import list_views

urlpatterns = (
    selia.urlpatterns +
    annotator.urlpatterns +
    create_views.urlpatterns +
    detail_views.urlpatterns +
    list_views.urlpatterns
)
