from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

import django_filters

from irekua_database.models import User
from selia_registration.forms import EmailUserForm
from selia_registration.utils import email_users


class UserFilter(django_filters.FilterSet):
    id = django_filters.ModelMultipleChoiceFilter(
        queryset=User.objects.all(),
        to_field_name='id',
        field_name='id')

    class Meta:
        model = User
        fields = [
            'collection_users',
            'collection_administrators',
            'is_superuser',
            'is_developer',
            'is_curator',
            'collectiontype',
        ]


class EmailUserView(LoginRequiredMixin, FormView):
    template_name = 'selia_registration/email_user.html'
    form_class = EmailUserForm
    success_url = 'email_user_done'

    def get_userset(self):
        return UserFilter(self.request.GET, queryset=User.objects.all()).qs

    def get_context_data(self, *args, **kwargs):
        return {
            'userset': self.get_userset(),
            **super().get_context_data(*args, **kwargs),
        }

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        userset = self.get_userset()
        sender = self.request.user
        email_users(subject, message, sender, userset)
        return super().form_valid(form)

    def get_success_url(self):
        baseurl = reverse(self.success_url)
        query = self.request.GET.copy()
        querystr = query.urlencode(safe='/')
        return f'{baseurl}?{querystr}'


class EmailUserDoneView(LoginRequiredMixin, TemplateView):
    template_name = 'selia_registration/email_user_done.html'
