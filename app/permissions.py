from rest_framework import permissions
from .models import Tasks

class IsTaskOwner(permissions.BasePermission):

  def has_permission(self, request, view):
    try:
      t = Tasks.objects.get(pk=view.kwargs['pk'])
    except:
      return False
      
    if t.user_id.id == request.user.id:
      return True 
    else:
      return False