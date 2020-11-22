from django.shortcuts import reverse
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from irekua_database.models import User
from irekua_collections.models import Collection

from irekua_permissions.data_collections import data_collections as permissions


def create_administrator_view(request):
    collection = get_object_or_404(Collection, name=request.GET.get('collection'))
    user = get_object_or_404(User, pk=request.GET.get('user', None))

    if not permissions.add_admin(request.user, collection=collection):
        return render(request, 'selia_templates/generic/no_permission.html')

    collection.add_administrator(user)
    return redirect(reverse('selia_managers:collection_detail', args=[collection.pk]))
