from rest_framework.permissions import BasePermission


class IsHasNotAnyRoleOrStudent(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and
            not request.user.is_student and
            not request.user.is_advisor or
            request.user.is_authenticated and
            request.user.is_student
        )


class IsHasNotAnyRoleOrAdvisor(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and
            not request.user.is_student and
            not request.user.is_advisor or
            request.user.is_authenticated and
            request.user.is_advisor
        )


class IsStudent(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and
            request.user.is_student
        )


class IsAdvisor(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and
            request.user.is_advisor
        )
