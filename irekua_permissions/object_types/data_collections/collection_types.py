from irekua_collections.models import CollectionType


def create(user, **kwargs):
    return user.is_superuser


def list(user, **kwargs):
    if user.is_superuser:
        return True

    return CollectionType.objects.filter(administrators=user).exists()


def queryset(user, **kwargs):
    if user.is_superuser:
        return CollectionType.objects.all()

    return CollectionType.objects.filter(administrators=user).distinct()


def view(user, collection_type=None, **kwargs):
    if collection_type is None:
        return False

    if user.is_superuser:
        return True

    return collection_type.administrators.filter(id=user.id).exists()


def change(user, collection_type=None, **kwargs):
    if collection_type is None:
        return False

    return user.is_superuser


def delete(user, collection_type=None, **kwargs):
    if collection_type is None:
        return False

    return user.is_superuser


__all__ = ['view', 'list', 'change', 'create', 'delete', 'queryset']
