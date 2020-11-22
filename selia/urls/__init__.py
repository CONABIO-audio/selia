from django.urls import path

from . import selia

# from . import create_views
# from . import detail_views
# from . import list_views

urlpatterns = (
    selia.urlpatterns
    # + create_views.urlpatterns
    # + detail_views.urlpatterns
    # + list_views.urlpatterns
)
