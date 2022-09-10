from rest_framework.permissions import IsAuthenticated, SAFE_METHODS


class IsOwnerOrReadOnly(IsAuthenticated):
    """
    Custom permission to only allow creator of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method is SAFE_METHODS:
            return True
        return request.user == obj.author

class IsOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user