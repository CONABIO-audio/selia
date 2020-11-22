from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.shortcuts import get_object_or_404
from irekua_permissions.object_types.data_collections import (
    collection_types as permissions)
from irekua_collections.models import Collection
from irekua_database.models import User


def delete_administrator(request, pk=None):
    collection = get_object_or_404(Collection, pk=pk)
    user = get_object_or_404(User, pk=request.GET.get('administrator', None))
    collection_type = collection.collection_type

    if not permissions.view(request.user, collection_type=collection_type):
        return render(request, 'selia_templates/generic/no_permission.html')

    collection.remove_administrator(user)
    return redirect(reverse('selia_managers:collection_detail', args=[pk]))
