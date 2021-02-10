from django.shortcuts import render
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from knox.models import AuthToken


class RegisterView(GenericAPIView):
  serializer_class = RegisterSerializer

  def post(self, request):
    serializer = self.serializer_class(data = request.data)
    if serializer.is_valid():
      user = serializer.save()
      return Response(self.serializer_class(user).data, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
  serializer_class = LoginSerializer

  def post(self, request):
    serializer = self.serializer_class(data = request.data)
    if serializer.is_valid():
      user = serializer.validated_data
      return Response({'user':UserSerializer(user).data, \
                       'token':AuthToken.objects.create(user)[1]}, \
                        status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    