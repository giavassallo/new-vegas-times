from rest_framework.permissions import BasePermission


class IsJournalist(BasePermission):
    """
    Only journalists can create articles.
    """

    def has_permission(self, request, view):

        return request.user.role == "journalist"


class IsEditor(BasePermission):
    """
    Only editors can approve or delete articles.
    """

    def has_permission(self, request, view):

        return request.user.role == "editor"


class IsReader(BasePermission):
    """
    Readers can only view articles.
    """

    def has_permission(self, request, view):

        return request.user.role == "reader"