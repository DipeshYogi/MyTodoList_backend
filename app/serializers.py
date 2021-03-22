from rest_framework import serializers
from .models import Tasks


class TaskSerializer(serializers.ModelSerializer):
  user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())

  class Meta:
    model = Tasks
    exclude = ['created_on']

  def create(self, validated_data):
    return Tasks.objects.create(**validated_data)


class TaskInfoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tasks
    fields = '__all__'