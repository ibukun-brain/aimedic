from rest_framework import permissions


class IsPractitionerOrReadOnly(permissions.BasePermission):
    message = "You are not a practitionr."
    """
    Object-level permission to only allow wallet users/owners of an object
    to access the wallet. Assumes the model instance has an `user` attribute.
    """

    def has_permission(self, request, view):
        return request.user.is_practitioner

    def has_object_permission(self, request, view, obj):

        # if request.method in permissions.SAFE_METHODS:
        #     return True
        # Instance must have an attribute named `user`.
        return obj.practitioner == request.user.practitioner
