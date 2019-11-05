from django import forms
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.utils.translation import gettext as _

from irekua_database.models import Collection
from irekua_database.models import User

from selia.views.create_views.create_base import SeliaCreateView
from irekua_permissions.data_collections import (
    users as user_permissions)


class SelectUserForm(forms.Form):
    email = forms.EmailField(
        label=_('User email'))


class SelectCollectionUserUserView(SeliaCreateView):
    template_name = 'selia/create/collection_users/select_user.html'
    prefix = 'user'
    form_class = SelectUserForm

    def get_objects(self):
        if not hasattr(self, 'collection'):
            self.collection = Collection.objects.get(
                name=self.request.GET['collection'])

    def has_view_permission(self):
        user = self.request.user
        return user_permissions.create(user, collection=self.collection)

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs.pop('instance')
        return form_kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection'] = self.collection
        return context

    def save_form(self, form):
        try:
            return User.objects.get(
                email=form.cleaned_data['email'])
        except User.DoesNotExist:
            msg = _(
                'No user with this email was found'
            )
            raise forms.ValidationError({'email': msg})

    def redirect_on_success(self):
        url = reverse('selia:create_collection_user')
        query = self.request.GET.copy()
        query['user'] = self.object.pk

        full_url = '{url}?{query}'.format(url=url, query=query.urlencode())
        return redirect(full_url)
