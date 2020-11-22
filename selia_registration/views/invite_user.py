from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from selia_registration.forms import InviteUserForm
from selia_registration.utils import invite_user


class InviteUserView(LoginRequiredMixin,FormView):
    template_name = 'selia_registration/invite_user.html'
    form_class = InviteUserForm
    success_url = 'invite_user_done'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        sender = self.request.user.username

        new_user = invite_user(email, sender, message=message)
        self.new_user_id = new_user.id
        return super().form_valid(form)

    def get_success_url(self):
        baseurl = reverse(self.success_url)
        query = self.request.GET.copy()
        query['user'] = self.new_user_id
        querystr = query.urlencode(safe='/')
        return f'{baseurl}?{querystr}'


class InviteUserDoneView(LoginRequiredMixin, TemplateView):
    template_name = 'selia_registration/invite_user_done.html'
