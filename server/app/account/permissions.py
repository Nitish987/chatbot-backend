from django.conf import settings
from rest_framework import permissions


# Api Request valid permission
class IsRequestValid(permissions.BasePermission):
    message = 'Something went wrong! Please try again.'

    def has_permission(self, request, view):
        key = request.META.get('HTTP_AAK')
        if key == settings.APP_API_KEY:
            return True
        return False

# Account Creation valid permission
class IsAccountCreationKeyValid(permissions.BasePermission):
    message = 'Something went wrong! Please try again.'

    def has_permission(self, request, view):
        key = request.META.get('HTTP_ACK')
        if key == settings.ACCOUNT_CREATION_KEY:
            return True
        return False