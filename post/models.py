from django.db import models

# Create your models here.
from user_profile.models import UserProfile


class Post(models.Model):
    # This sets the content
    content = models.TextField(max_length=1000)
    # This sets the date when the post is created
    created = models.DateTimeField(auto_now_add=True)
    # This sets the date for when the post was updated the last time
    last_updated = models.DateTimeField(auto_now=True)
    # This sets the posted_by field, to see who the author of a post ist
    posted_by = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='posts')
    # This sets the field that shows all the users that liked this post
    liked_by = models.ManyToManyField(to=UserProfile, related_name='liked_posts', blank=True)
    # This sets the field that shows all the users that shared this post
    shared_by = models.ManyToManyField(to=UserProfile, related_name='shared_posts', blank=True)

    def __str__(self):
        return f'ID: {self.id} | Content: {self.content[:30]}... | by: {self.posted_by.user.username}'