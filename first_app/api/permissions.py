from rest_framework import permissions

class IsParentOrExpert(permissions.BasePermission):
    def has_permission(self, request, obj):
        if request.user.user.account_type  == 'Parent':
            return False
        else:
            return True