from django import forms
from django.utils.translation import gettext_lazy as _
import pycountry

from irekua_autocomplete.utils import get_autocomplete_widget
from irekua_database.models import User
from irekua_database.models import Institution
from selia.views.detail_views.base import SeliaDetailView


INSTITUTION_FIELDS = [
    'institution_name',
    'institution_code',
    'subdependency',
    'country',
    'postal_code',
    'address',
    'website',
]



class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = INSTITUTION_FIELDS


class DetailUserView(SeliaDetailView):
    model = User

    template_name = 'selia/detail/user.html'

    help_template = 'selia/help/user_home.html'
    detail_template = 'selia/details/user.html'
    summary_template = 'selia/summaries/user.html'
    update_form_template = 'selia/update/user.html'

    def get_form_class(self):
        COUNTRIES = (
            (country.alpha_2, country.name) for country in pycountry.countries
        )

        class Form(forms.ModelForm):
            institution_name = forms.CharField(
                max_length=256,
                label=_('Institution name'),
                required=False)
            institution_code = forms.CharField(
                max_length=64,
                label=_('Institution code'),
                required=False)
            subdependency = forms.CharField(
                max_length=256,
                label=_('Subdependency'),
                help_text=_('Subdependency at institution'),
                required=False)
            country = forms.ChoiceField(
                choices=COUNTRIES,
                label=_('Country'),
                required=False)
            postal_code = forms.CharField(
                max_length=8,
                label=_('Postal code'),
                required=False)
            address = forms.CharField(
                required=False,
                label=_('Address'))
            website = forms.URLField(
                required=False,
                label=_('Website'))

            class Meta:
                model = User
                fields = [
                    'username',
                    'first_name',
                    'last_name',
                    'email',
                    'institution'
                ]

                widgets = {'institution': get_autocomplete_widget(name='institutions')}
        return Form

    def get_initial(self):
        initial = super().get_initial()

        if self.object.institution:
            initial['institution_name'] = self.object.institution.institution_name
            initial['institution_code'] = self.object.institution.institution_code
            initial['subdependency'] = self.object.institution.subdependency
            initial['postal_code'] = self.object.institution.postal_code
            initial['address'] = self.object.institution.address
            initial['website'] = self.object.institution.website
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['has_institution'] = (self.object.institution is None)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)

        institution_data = {
            field: form.cleaned_data[field]
            for field in INSTITUTION_FIELDS}

        print('captured data', institution_data)
        institution_form = InstitutionForm(institution_data.copy())
        institution = None
        try:
            institution = Institution.objects.get(
                institution_name=institution_data.pop('institution_name'),
                subdependency=institution_data.pop('subdependency'))

            institution.institution_code = institution_data.pop('institution_code')
            institution.postal_code = institution_data.pop('postal_code')
            institution.address = institution_data.pop('address')
            institution.website = institution_data.pop('website')
            institution.country = institution_data.pop('country')
            institution.save()

        except Institution.DoesNotExist:
            if institution_form.is_valid():
                institution = institution_form.save()

        if institution:
            self.object.institution = institution
            self.object.save()

        return response

    def get_object(self):
        return self.request.user

    def has_delete_permission(self):
        return False

    def has_view_permission(self):
        return self.request.user.is_authenticated
