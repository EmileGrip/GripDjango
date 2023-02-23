from rest_framework import permissions
from .models import User

class IsUserOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user


class IsAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        print('ssssssIsAdminsssssssssss',request.user.pk)
  
        if User.objects.filter(is_company=True,pk=request.user.pk).exists():
            print('ssssssIsAdminsssssssssss')
            return True

        return False
    

    def has_object_permission(self, request, view, obj):

        print('sssskkssssss')

        if User.objects.filter(is_manager=True,pk=request.user.pk).exists():
            print('ssssssIsAdminsssssssssss')
            return True

        return False

class IsManager(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        print('ssssssIsAdminsssssssssss')

        if User.objects.filter(is_manager=True,pk=request.user.pk).exists():
            print('ssssssIsManagersssssssssss')
            return True

        return False