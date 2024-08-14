from rest_framework.permissions  import BasePermission

class IsAdminOrReadOnly(BasePermission):
    #custom permission to  only allow  admins to edit an object.
    #non-admin  users can only  view the objects

    def has_permission(self, request, view):
        if view.action  in ['list','retrieve']:
            return True
        return request.user.is_superuser
    
    
