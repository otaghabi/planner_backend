from rest_framework.permissions import BasePermission


class IsHasNotAnyRole(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and
            not request.user.is_student and
            not request.user.is_advisor
        )
