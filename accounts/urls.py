from django.urls import path, include
from .views import RegisterView, LoginView, UserUpdateView
from knox.views import LogoutView

urlpatterns = [
  path('register/', RegisterView.as_view(), name = 'register'),
  path('login/', LoginView.as_view(), name = 'login'),
  path('logout/', LogoutView.as_view(), name = 'logout'),
  path('user-update/', UserUpdateView.as_view(), name = 'update_user'),
]