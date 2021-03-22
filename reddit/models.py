from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


def upload_to(instance, filename):
  return f'posts/{filename}'


class Posts(models.Model):
  user_id = models.ForeignKey(get_user_model(), \
                          on_delete=models.CASCADE, related_name='my_posts')
  title = models.CharField(max_length=50)
  desc = models.CharField(max_length=2000, blank=True, null=True)
  img = models.ImageField(upload_to=upload_to, null=True, blank=True)
  created_on = models.DateField(auto_now=True)

  class Meta:
    verbose_name_plural= 'Posts'

  def __str__(self):
    return self.user_id.username + ' :' + self.title[:15] + '...'


class Tags(models.Model):
  post_id = models.ForeignKey(Posts, on_delete = models.CASCADE, \
                              related_name='post_tags')
  tag = models.CharField(max_length=30)

  class Meta:
    verbose_name_plural = 'Tags'

  def save(self, *args, **kwargs):
    self.tag = self.tag.upper()
    super().save(*args, **kwargs)

  def __str__(self):
    return str(self.post_id.id) + ': Tags' 


class Like(models.Model):
  post = models.ForeignKey(Posts, on_delete=models.CASCADE, \
                              related_name='post_likes')
  liked_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                               related_name='my_likes')
  like_choices = (
    ('true', 'true'),
    ('false', 'false'),
    ('none', 'none')
    )
  is_liked = models.CharField(choices = like_choices, max_length = 20)
  is_disliked = models.CharField(choices = like_choices, max_length = 20)

  def save(self, *args, **kwargs):
    try:
      l_instance = Like.objects.get(post= self.post, liked_by = self.liked_by) 
      if l_instance:
        l_instance.delete()
        super().save(*args, **kwargs)
    except Like.DoesNotExist:
      super().save(*args, **kwargs)

  def __str__(self):
    return str(self.post) + ' likes'


class Comment(models.Model):
  post = models.ForeignKey(Posts, on_delete=models.CASCADE, \
                           related_name = 'post_comments')
  author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, \
                             related_name='user_comments')
  comm = models.CharField(max_length = 500)
  created_on = models.DateField(auto_now=True)
  parent = models.ForeignKey('self', null=True, blank=True, \
                            on_delete=models.SET_NULL, related_name='replies')

  def __str__(self):
    return str(self.post.id) + ' - commented by ' + str(self.author.username)


class CommentLike(models.Model):
  comment = models.ForeignKey(Comment, on_delete=models.CASCADE, \
                               related_name='comments_liked')
  liked_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
  like_choices = (
    ('true', 'true'),
    ('false', 'false'),
    ('none', 'none')
    )
  is_liked = models.CharField(choices = like_choices, max_length = 20)
  is_disliked = models.CharField(choices = like_choices, max_length = 20)

  def save(self, *args, **kwargs):
    if self.is_liked == self.is_disliked and self.is_liked != 'none':
      raise ValidationError('IsLiked and IsDisliked cannot be true \
                             at the same time')

    try:
      like_instance = CommentLike.objects.get(comment=self.comment, liked_by=self.liked_by)
      if like_instance:
        like_instance.delete()
        super().save(*args, **kwargs)
    except CommentLike.DoesNotExist:
      super().save(*args, **kwargs)

  def __str__(self):
    return str(self.comment.id) + ' comment likes'



