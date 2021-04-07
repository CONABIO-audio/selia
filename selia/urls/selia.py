from django.urls import path
from selia import views
from . import list_views 
from . import detail_views
from . import create_views

SELIA_URLS = (
    list_views.urlpatterns +
    detail_views.urlpatterns +
    create_views.urlpatterns
)

urlpatterns = [
    path('', views.home, name='home'),
] + SELIA_URLS
