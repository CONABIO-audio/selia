from django.urls import path
from selia.views.create_views import users


urlpatterns = [
    path(
        'users/create/',
        users.CreateUserManager.as_view(),
        name='create_user'),
    path(
        'users/create/1/',
        users.CreateUserView.as_view(),
        name='create_user_create_form'),
]
