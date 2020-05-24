from django.shortcuts import redirect
from django.urls import reverse

from irekua_database.models import Collection
from irekua_database.models import LicenceType

from selia.views.create_views.select_base import SeliaSelectView
from irekua_permissions import licences as licence_permissions


class SelectLicenceTypeView(SeliaSelectView):
    template_name = 'selia/create/licences/select_type.html'
    prefix = 'licence_type'

    def get_objects(self):
        if not hasattr(self, 'collection'):
            self.collection = Collection.objects.get(name=self.request.GET['collection'])

    def has_view_permission(self):
        user = self.request.user
        return licence_permissions.create(user, collection=self.collection)

    def should_redirect(self):
        collection_type = self.collection.collection_type

        if collection_type.restrict_licence_types:
            self.licence_types = collection_type.licence_types.all()
        else:
            self.licence_types = LicenceType.objects.all()

        return self.licence_types.count() == 1

    def handle_single_type_redirect(self):
        url = reverse('selia:create_licence')

        query = self.request.GET.copy()
        query['licence_type'] = self.licence_types.first().name
        full_url = '{url}?{query}'.format(
            url=url,
            query=query.urlencode())
        return redirect(full_url)

    def get_list_context_data(self):
        return self.licence_types

    def get(self, *args, **kwargs):
        self.get_objects()

        if not self.has_view_permission():
            return self.no_permission_redirect()

        if self.should_redirect():
            return self.handle_single_type_redirect()

        return super().get(*args, **kwargs)

    def get_context_data(self):
        context = super().get_context_data()
        context['collection'] = self.collection
        return context
