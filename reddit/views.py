from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import Posts, Tags, Like, Comment, CommentLike
from .serializers import PostSerializer, LikeSerializer, PostCreateSerializer,\
                         GetPostSerializer, CommentSerializer, GetCommentSerializer,\
                         GetCommentLikeSerializer, PostCommentLikeSerializer                         
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class PostViewSets(viewsets.ViewSet):

  permission_classes = [permissions.IsAuthenticated,]

  def get_serializer_class(self):
    if self.action in ('create', 'update'):
      return PostCreateSerializer
    else:
      return PostSerializer

  @method_decorator(cache_page(60*5))
  def list(self, request):
    queryset = Posts.objects.all()
    serializer = GetPostSerializer(queryset, many=True)
    return Response(serializer.data)
  
  def create(self, request):
    serializer_class = self.get_serializer_class()
    serializer = serializer_class(data = request.data, partial=True)
    if serializer.is_valid():
      post_data = serializer.save(user_id = request.user.id)
      return Response(PostSerializer(post_data).data)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

  def retrieve(self, request, pk):
    serializer_class = self.get_serializer_class()
    try:
      post = Posts.objects.get(pk=pk)
      serializer = serializer_class(post)
      return Response(serializer.data)
    except Posts.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)
  
  def destroy(self, request, pk):
    try:
      post = Posts.objects.get(pk = pk)
      post.delete()
      return Response({"msg":f"{pk} Deleted"}, status=status.HTTP_200_OK)
    except Posts.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

  def update(self, request, pk):
    serializer_class = self.get_serializer_class()
    try:
      post_instance = Posts.objects.get(pk = pk)
      serializer = serializer_class( post_instance, data = request.data, \
                                     partial = True)
      if serializer.is_valid():
        post_data = serializer.save()
        return Response(PostSerializer(post_data).data)
      return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    except Posts.DoesNotExist:
      return Response(status= status.HTTP_404_NOT_FOUND)
      

class LikeViewSets(viewsets.ViewSet):
  serializer_class = LikeSerializer
  permission_classes = [permissions.IsAuthenticated,]

  def list(self, request):
    queryset = Like.objects.all()
    serializer = self.serializer_class(queryset, many=True)
    return Response(serializer.data)

  def create(self, request):
    serializer = self.serializer_class(data = request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class CommentViewSets(viewsets.ViewSet):
  serializer_class = CommentSerializer
  permission_classes = [permissions.IsAuthenticated, ]

  def list(self, request):
    queryset = Comment.objects.all()
    serializer = self.serializer_class(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def retrieve(self, request, pk):
    try:
      queryset = Comment.objects.filter(post = pk)
      serializer = GetCommentSerializer(queryset, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Comment.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

  def create(self, request):
    # import pdb; pdb.set_trace()
    serializer = self.serializer_class(data=request.data, \
                                   partial=True)
    if serializer.is_valid():
      comment = serializer.save(user_id = request.user)
      return Response(GetCommentSerializer(comment).data, \
                      status=status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class CommentLikeViewSets(viewsets.ViewSet):
  permission_classes = [permissions.IsAuthenticated,]

  def list(self, request):
    queryset = CommentLike.objects.all()
    serializer = GetCommentLikeSerializer(queryset, many=True)
    return Response(serializer.data, status = status.HTTP_200_OK)

  def retrieve(self, request, pk):
    queryset = []
    try:
      posts = Posts.objects.get(id = pk)
      for i in posts.post_comments.all():
        for j in i.comments_liked.all():
          queryset.append(j)
      serializer = GetCommentLikeSerializer(queryset, many=True)
      return Response(serializer.data, status = status.HTTP_200_OK)
    except Posts.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

  def create(self, request):
    permission_classes = [permissions.IsAuthenticated,]
    serializer = PostCommentLikeSerializer(data = request.data)
    if serializer.is_valid():
      liked_data = serializer.save(liked_by=request.user)
      return Response(GetCommentLikeSerializer(liked_data).data, status=status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





    

