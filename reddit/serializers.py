from rest_framework import serializers
from .models import Posts, Tags, Like, Comment, CommentLike
from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tags 
    fields = ['id','tag']


class PostSerializer(serializers.ModelSerializer):
  post_tags = TagSerializer(many=True)

  class Meta:
    model = Posts
    fields = ['id', 'user_id', 'title', 'desc', 'img', 'created_on', 'post_tags']


class PostCreateSerializer(serializers.Serializer):
  user_id = serializers.IntegerField()
  title = serializers.CharField()
  desc = serializers.CharField(required=False)
  img = serializers.ImageField(required=False)
  post_tags = serializers.CharField(required=False)

  def create(self, validated_data):  
    user = get_user_model().objects.get(pk = validated_data.get('user_id'))
    post = Posts.objects.create(user_id = user, title = validated_data.get('title'),\
           desc = validated_data.get('desc'), img = validated_data.get('img'))
    if validated_data.get('post_tags'):
      tag_data = validated_data.pop('post_tags')
      tag_data = tag_data.split(',')
      for i in tag_data:
        Tags.objects.create(post_id=post, tag=i)

    return post

  def update(self, instance, validated_data):
    if validated_data.get('post_tags'):
      tag_data = validated_data.pop('post_tags')
      try:
        tag_instance = Tags.objects.filter(post_id = instance.id)
        tag_instance.delete()
      except:
        pass
      finally:
        tag_data = tag_data.split(',')
        for i in tag_data:
          Tags.objects.create(post_id=instance, tag=i)

    instance.title = validated_data.get('title', instance.title)
    instance.desc = validated_data.get('desc', instance.desc)
    instance.img = validated_data.get('img', instance.img)      
    
    instance.save()

    return instance    


class LikeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Like
    fields = ['post', 'liked_by', 'is_liked', 'is_disliked']


class GetPostSerializer(serializers.ModelSerializer):
  username = serializers.CharField(source='user_id.username', read_only=True)
  post_tags = TagSerializer(many=True)

  class Meta:
    model = Posts
    fields = ['id', 'title', 'desc', 'img', 'created_on', 'post_tags', 'username']


class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = ['id', 'post', 'author', 'comm', 'created_on', 'parent']

  def create(self, validated_data):
    # import pdb; pdb.set_trace()
    comment = Comment.objects.create(post = validated_data.get('post'),
                                    author = validated_data.get('user_id'),
                                    comm = validated_data.get('comm'),
                                    parent = validated_data.get('parent')
                                  )
    return comment


class GetCommentSerializer(serializers.ModelSerializer):
  username = serializers.CharField(source='author.username', read_only=True)

  class Meta:
    model = Comment
    fields = ['id', 'post', 'username', 'comm', 'created_on', 'parent']


class GetCommentLikeSerializer(serializers.ModelSerializer):
  username = serializers.CharField(source='liked_by.username', read_only=True)

  class Meta:
    model = CommentLike
    fields = ['comment', 'username', 'is_liked', 'is_disliked']


class PostCommentLikeSerializer(serializers.ModelSerializer):
  class Meta:
    model = CommentLike
    fields = ['comment', 'is_liked', 'is_disliked']

  def create(self, validated_data):
    if validated_data.get('is_liked') == validated_data.get('is_disliked') and \
       validated_data.get('is_liked') != 'none':
      raise serializers.ValidationError("Liked and Disliked cannot be same.")

    comment_like = CommentLike.objects.create(**validated_data)
    return comment_like