from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate


class RegisterSerializer(serializers.ModelSerializer):
  class Meta:
    model = get_user_model()
    fields = ['username', 'email', 'password']

  def create(self, validated_data):
    user = get_user_model().objects.create_user(
                                validated_data.get('username'),
                                validated_data.get('email'),
                                validated_data.get('password')
    )
    return user


class LoginSerializer(serializers.Serializer):
  username = serializers.CharField(max_length=25)
  password = serializers.CharField(max_length=25)

  def validate(self, data):
    user = authenticate(**data)
    if user and user.is_active:
      return user
    else:
      raise serializers.ValidationError("Invalid Credentials")


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = get_user_model()
    fields = ['id', 'username', 'email']

  def update(self, instance, validated_data):
    instance.username = validated_data.get('username', instance.username)
    instance.email = validated_data.get('email', instance.email)
    instance.save()

    return instance
  
