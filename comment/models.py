from django.db import models

from post.models import Post
from user_profile.models import UserProfile


# Create your models here.
class Comment(models.Model):
    # This sets the content field
    content = models.CharField(max_length=1000)
    # This sets the post relation
    user_profile = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='comments')
    # This sets the post field
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'ID: {self.id} | Comment: {self.content} | by: {self.user_profile.user.username}'