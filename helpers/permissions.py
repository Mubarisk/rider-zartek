from rest_framework.permissions import BasePermission
from user.models import User


class IsRider(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == User.UserTypes.RIDER


class IsDriver(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == User.UserTypes.DRIVER
