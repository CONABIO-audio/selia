from django.urls import path
from selia_about import views


urlpatterns = [
    path('', views.about_selia, name='selia'),
    path('irekua/', views.about_irekua, name='irekua'),
    path('contact/', views.about_contact, name='contact'),
    path('collections/', views.about_collections, name='collections')
]
