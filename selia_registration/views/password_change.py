from django.contrib.auth import views


class PasswordChangeView(views.PasswordChangeView):
    template_name = 'selia_registration/password_change_form.html'
    success_url = 'done'

    def get_success_url(self):
        url = super().get_success_url()
        query = self.request.GET.urlencode(safe='/')
        return f'{url}?{query}'
