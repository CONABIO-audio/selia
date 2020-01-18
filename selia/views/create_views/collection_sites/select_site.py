from django import forms
from django.shortcuts import redirect
from django.shortcuts import reverse

from irekua_database.models import Collection
from irekua_database.models import Site
from irekua_database.models import SiteType
from irekua_autocomplete.utils import get_autocomplete_widget

from irekua_filters import sites as site_utils
from irekua_permissions.data_collections import sites as site_permissions
from selia.views.create_views.create_base import SeliaCreateView
from selia.views.utils import SeliaList


class SelectCollectionSiteSiteView(SeliaCreateView):
    model = Site
    template_name = 'selia/create/collection_sites/select_site.html'
    prefix = 'site'
    create_url = 'selia:create_collection_site'

    def get_form_class(self):
        class SiteCreateForm(forms.ModelForm):
            class Meta:
                model = Site
                fields = [
                    'latitude',
                    'longitude',
                    'altitude',
                    'name',
                    'locality',
                ]

                widgets = {
                    'locality': get_autocomplete_widget(name='localities')
                }

        return SiteCreateForm

    def has_view_permission(self):
        user = self.request.user
        return site_permissions.create(user, collection=self.collection)

    def get_objects(self):
        if not hasattr(self, 'collection'):
            self.collection = Collection.objects.get(name=self.request.GET['collection'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection'] = self.collection
        context['site_type'] = SiteType.objects.get(pk=self.request.GET['site_type'])
        context['list'] = self.get_site_list()
        context['prefix'] = self.prefix
        context['create_url'] = self.create_url

        return context

    def redirect_on_success(self):
        url = reverse('selia:create_collection_site')
        query = self.request.GET.copy()
        query['site'] = self.object.pk

        full_url = '{url}?{query}'.format(url=url, query=query.urlencode())
        return redirect(full_url)

    def get_fields_to_remove_on_sucess(self):
        return []

    def get_site_list(self):
        sites = (
            Site.objects
            .filter(created_by=self.request.user)
            .exclude(collectionsite__collection=self.collection)
        )

        class SiteList(SeliaList):
            prefix = 'sites'

            filter_class = site_utils.Filter
            search_fields = site_utils.search_fields
            ordering_fields = site_utils.ordering_fields

            queryset = sites

            list_item_template = 'selia/select_list_items/sites.html'
            filter_form_template = 'selia/filters/site.html'

        site_list = SiteList(self.request)
        return site_list.get_context_data()
