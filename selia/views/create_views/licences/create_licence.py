from django import forms

from irekua_database.models import Collection
from irekua_database.models import Licence
from irekua_database.models import LicenceType

from irekua_permissions import licences as licence_permissions
from selia.views.create_views.create_base import SeliaCreateView
from selia.forms.json_field import JsonField


class CreateLicenceForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = Licence
        fields = [
            'licence_type',
            'document',
            'metadata',
            'collection',
        ]


class CreateLicenceView(SeliaCreateView):
    template_name = 'selia/create/licences/create_form.html'
    success_url = 'selia:collection_licences'

    model = Licence
    form_class = CreateLicenceForm

    def get_objects(self):
        if not hasattr(self, 'collection'):
            self.collection = Collection.objects.get(
                pk=self.request.GET['collection'])

        if not hasattr(self, 'licence_type'):
            self.licence_type = LicenceType.objects.get(
                name=self.request.GET['licence_type'])

    def has_view_permission(self):
        user = self.request.user
        return licence_permissions.create(user, collection=self.collection)

    def get_initial(self, *args, **kwargs):
        return {
            'collection': self.collection,
            'licence_type': self.licence_type,
        }

    def get_success_url_args(self):
        return [self.request.GET['collection']]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['collection'] = self.collection
        context['licence_type'] = self.licence_type

        context['form'].fields['metadata'].update_schema(
            self.licence_type.metadata_schema)
        return context
