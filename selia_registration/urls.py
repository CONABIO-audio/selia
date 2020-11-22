from django.urls import path
from django.urls import re_path
from django.contrib.auth import views as auth_views

from selia_registration import views


urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='selia_registration/login.html'),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='selia_registration/password_reset_form.html',
            email_template_name='selia_registration/password_reset_email.html',
            subject_template_name='selia_registration/password_reset_subject.txt'),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='selia_registration/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        r'password_reset/confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='selia_registration/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'password_reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='selia_registration/password_reset_complete.html'),
        name='password_reset_complete'
    ),
    path(
        'password_change/',
        views.PasswordChangeView.as_view(),
        name='password_change'
    ),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='selia_registration/password_change_done.html'
        ),
        name='password_change_done'
    ),
    path(
        'invite/',
        views.InviteUserView.as_view(),
        name='invite'),
    path(
        'invite/done/',
        views.InviteUserDoneView.as_view(),
        name='invite_user_done'),
    path(
        'email/',
        views.EmailUserView.as_view(),
        name='email_user'),
    path(
        'email/done/',
        views.EmailUserDoneView.as_view(),
        name='email_user_done'),
]
