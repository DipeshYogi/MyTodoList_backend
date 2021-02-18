from django.shortcuts import render
from .models import Tasks
from .serializers import TaskSerializer, TaskInfoSerializer
from rest_framework import viewsets
from rest_framework import permissions, status
from .permissions import IsTaskOwner


class TaskViewSet(viewsets.ModelViewSet):

  def get_queryset(self):
    return Tasks.objects.filter(user_id=self.request.user.id)

  def get_permissions(self):
    if self.request.method == 'PUT':
      self.permission_classes = [IsTaskOwner,]
    return super().get_permissions()

  def get_serializer_class(self):
    if self.action in ('create', 'update'):
      return TaskSerializer
    else:
      return TaskInfoSerializer 






