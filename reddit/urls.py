from django.urls import path, include
from .views import PostViewSets, LikeViewSets, CommentViewSets, \
                   CommentLikeViewSets
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostViewSets, 'posts')
router.register(r'likes', LikeViewSets, 'likes')
router.register(r'comments', CommentViewSets, 'comments')
router.register(r'comment-like', CommentLikeViewSets, 'comment-like')


urlpatterns = [
  path('', include(router.urls)),
]