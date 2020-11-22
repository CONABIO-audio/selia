from selia.views.create_views.manager_base import CreateManagerBase


class CreateSiteManager(CreateManagerBase):
    required_get_parameters = []
    manager_name = "selia_user_home:create_site"

    def view_from_request(self):
        if "geometry_type" not in self.request.GET:
            return "selia_user_home:create_site_select_geometry_type"

        return "selia_user_home:create_site_create_form"
