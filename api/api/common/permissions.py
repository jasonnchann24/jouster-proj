from rest_framework import permissions
from api.utils import user_is_admin


class IsOwner(permissions.BasePermission):
    """
    Only allow access to the object's owner.
    Pass the comparison field name as 'compare_field' when using.
    """

    compare_field = "user_id"
    admin_access = True

    def __init__(self, compare_field=None, admin_access=True):
        if compare_field:
            self.compare_field = compare_field
            self.admin_access = admin_access

    def has_object_permission(self, request, view, obj):
        owner_id = getattr(obj, self.compare_field, None)

        if self.admin_access and user_is_admin(request.user):
            return True

        return bool(owner_id == getattr(request.user, "id", None))
