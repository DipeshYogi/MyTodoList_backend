from django.contrib import admin
from .models import Posts, Tags, Like, Comment, CommentLike

admin.site.register(Posts)
admin.site.register(Tags)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(CommentLike)

