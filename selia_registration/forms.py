from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


class InviteUserForm(forms.Form):
    email = forms.EmailField(
        label=_('Email'),
        max_length=124)
    message = forms.CharField(
        label=_('Write a message'),
        max_length=500,
        widget=forms.Textarea,
        required=False)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        User = get_user_model()
        if User.objects.filter(email=email).exists():
            message = _(
                'A user with this email is already registered in Selia.'
            )
            self.add_error('email', message)


class EmailUserForm(forms.Form):
    subject = forms.CharField(
        label=_('Email subject'),
        max_length=64,
        required=True)
    message = forms.CharField(
        label=_('Write a message'),
        max_length=2048,
        widget=forms.Textarea,
        required=True)
