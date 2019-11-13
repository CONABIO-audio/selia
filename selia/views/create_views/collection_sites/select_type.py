from django.views.generic import TemplateView
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

from irekua_database.models import Collection
from irekua_database.models import SiteType
from irekua_permissions.data_collections import (
    sites as site_permissions)


class SelectCollectionSiteTypeView(TemplateView):
    no_permission_template = 'selia/no_permission.html'
    template_name = 'selia/create/collection_sites/select_type.html'

    def has_view_permission(self):
        user = self.request.user
        return site_permissions.create(user, collection=self.collection)

    def should_redirect(self):
        collection_type = self.collection.collection_type

        if collection_type.restrict_site_types:
            self.site_types = collection_type.site_types.all()
        else:
            self.site_types = SiteType.objects.all()

        return self.site_types.count() == 1

    def handle_single_type_redirect(self):
        url = reverse('selia:create_collection_site')
        full_url = '{url}?{query}&site_type={pk}'.format(
            url=url,
            query=self.request.GET.urlencode(),
            pk=self.site_types.first().pk)
        return redirect(full_url)

    def get_objects(self):
        self.collection = Collection.objects.get(name=self.request.GET['collection'])

    def no_permission_redirect(self):
        return render(self.request, self.no_permission_template)

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
        context['list'] = self.site_types
        return context
