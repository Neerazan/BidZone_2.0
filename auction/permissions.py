from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)



class IsUser(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in ['OPTIONS', 'HEAD']:
            return True
        
        return request.user.id == obj.user_id



# class IsProductOwner(permissions.IsAuthenticated):
#     def has_object_permission(self, request, view, obj):
#         if request.method in ['OPTIONS', 'HEAD']:
#             return True
        
#         return request.user.id == obj.customer.user_id