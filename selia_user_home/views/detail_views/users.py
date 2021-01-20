import pycountry
from django import forms
from django.utils.translation import gettext_lazy as _

from irekua_database.autocomplete import get_autocomplete_widget
from irekua_database.models import User
from irekua_database.models import Institution
from selia_templates.views import SeliaDetailView


INSTITUTION_FIELDS = [
    "institution_name",
    "institution_code",
    "country",
    "postal_code",
    "address",
    "website",
]


COUNTRIES = ((country.alpha_2, country.name) for country in pycountry.countries)


class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = INSTITUTION_FIELDS


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]


class DetailUserView(SeliaDetailView):
    model = User

    template_name = "selia_user_home/detail/users.html"
    help_template = "selia_user_home/help/users_detail.html"
    detail_template = "selia_user_home/details/users.html"
    summary_template = "selia_user_home/summaries/users.html"
    update_form_template = "selia_user_home/update/users.html"

    form_class = UserForm

    def get_institution_formset(self, kwargs):
        return None

    def get_context_data(self, kwargs):
        return {
            "institution_formset": self.get_institution_formset(kwargs)
            ** super().get_context_data(kwargs)
        }

    def get_object(self, *args, **kwargs):
        return self.request.user

    def has_delete_permission(self):
        return False

    def has_view_permission(self):
        return self.request.user.is_authenticated
