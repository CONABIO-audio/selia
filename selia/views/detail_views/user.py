from django import forms
from dal import autocomplete

from selia.views.detail_views.base import SeliaDetailView
from irekua_database.models import User


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'institution'
        ]

        widgets = {
            'institution': autocomplete.ModelSelect2(
                url='irekua_autocomplete:institutions_autocomplete',
                attrs={
                    'style': 'width: 100%;'
                }
            )
        }


class DetailUserView(SeliaDetailView):
    model = User
    form_class = UserUpdateForm

    template_name = 'selia/detail/user.html'

    help_template = 'selia/components/help/user_home.html'
    detail_template = 'selia/components/details/user.html'
    summary_template = 'selia/components/summaries/user.html'
    update_form_template = 'selia/components/update/user.html'

    def get_object(self):
        return self.request.user

    def has_delete_permission(self):
        return False

    def has_view_permission(self):
        return self.request.user.is_authenticated
