from django.views.generic import TemplateView
from django.shortcuts import render


class SeliaAnnotationView(TemplateView):
    no_permission_template = 'selia/no_permission.html'

    def has_view_permission(self):
        return self.request.user.is_authenticated

    def no_permission_redirect(self):
        return render(self.request, self.no_permission_template)

    def get(self, *args, **kwargs):
        if not self.has_view_permission():
            return self.no_permission_redirect()

        return super().get(*args, **kwargs)
