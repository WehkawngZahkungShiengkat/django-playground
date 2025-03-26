from django.db import models
from django.contrib.auth.models import User
from post.models import Post

# Create your models here.


class Comment(models.Model):
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"Post ID-{self.comment_post}'s Command ID-{self.id}"
