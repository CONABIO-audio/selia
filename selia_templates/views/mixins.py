from django.shortcuts import render


class SeliaPermissionsMixin:
    no_permission_template = "selia_templates/generic/no_permission.html"

    def get(self, *args, **kwargs):
        if not self.has_view_permission():
            return self.no_permission_redirect()

        return super().get(*args, **kwargs)

    def no_permission_redirect(self):
        return render(self.request, self.no_permission_template)

    def has_view_permission(self):
        return True