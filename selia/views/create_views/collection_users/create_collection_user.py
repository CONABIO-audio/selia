from django import forms

from selia.views.create_views.create_base import SeliaCreateView
from irekua_collections.models import Collection
from irekua_collections.models import CollectionTypeRole
from irekua_collections.models import CollectionUser
from irekua_database.models import Role
from irekua_database.models import User

from selia_templates.forms.json_field import JsonField


class CreateCollectionUserForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = CollectionUser
        fields = [
            'collection',
            'user',
            'role',
            'metadata',
        ]


class CreateCollectionUserView(SeliaCreateView):
    template_name = 'selia/create/collection_users/create_form.html'
    success_url = 'selia:collection_users'

    model = CollectionUser
    form_class = CreateCollectionUserForm

    def get_initial(self, *args, **kwargs):
        self.collection = Collection.objects.get(
            name=self.request.GET['collection'])
        self.user = User.objects.get(
            pk=self.request.GET['user'])
        self.role = Role.objects.get(
            pk=self.request.GET['role'])

        return {
            'collection': self.collection,
            'role': self.role,
            'user': self.user,
        }

    def get_success_url_args(self):
        return [self.request.GET['collection']]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['collection'] = self.collection
        context['selected_user'] = self.user
        context['role'] = self.role

        role_info = CollectionRole.objects.get(
            collection_type=self.collection.collection_type,
            role=self.role)
        context['role_info'] = role_info

        context['form'].fields['metadata'].update_schema(
            role_info.metadata_schema)
        return context
