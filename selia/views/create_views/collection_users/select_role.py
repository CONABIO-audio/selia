from django.shortcuts import redirect
from django.urls import reverse

from irekua_database.models import Collection

from selia.views.create_views.select_base import SeliaSelectView
from irekua_permissions.data_collections import (
    users as user_permissions)


class SelectCollectionUserRoleView(SeliaSelectView):
    template_name = 'selia/create/collection_users/select_role.html'
    prefix = 'role'

    def get_objects(self):
        if not hasattr(self, 'collection'):
            self.collection = Collection.objects.get(name=self.request.GET['collection'])

        if not hasattr(self, 'role_types'):
            self.role_types = self.collection.collection_type.roles.all()

    def has_view_permission(self):
        user = self.request.user
        return user_permissions.create(user, collection=self.collection)

    def should_redirect(self):
        return self.role_types.count() == 1

    def handle_single_type_redirect(self):
        url = reverse('selia:create_collection_user')

        query = self.request.GET.copy()
        query['role'] = self.role_types.first().pk
        full_url = '{url}?{query}'.format(
            url=url,
            query=query.urlencode())
        return redirect(full_url)

    def get_list_context_data(self):
        return self.role_types

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
