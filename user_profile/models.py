from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# This defines the path where this models files should be stored. In this case it refers to the avatar
def user_directory_path(instance, filename):
    # Here we define the path/sub-folder where this file should be stored. In this case it will be
    # /media-files/1/avatar.jpg for example.
    return f'{instance.id}/{filename}'


# Create your models here.
class UserProfile(models.Model):
    # This sets the username field
    # username = models.CharField(max_length=50, unique=True)
    # This sets the first name field
    first_name = models.CharField(max_length=50)
    # This sets the last name field
    last_name = models.CharField(max_length=50)
    # This connects the UserProfile to an actual User (from our custom user model)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='user_profile')
    # This sets the location field
    location = models.CharField(max_length=100)
    # This sets the about field
    about = models.TextField(max_length=500)
    # This sets the avatar/profile picture
    avatar = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    # This sets the phone number
    phone = models.CharField(max_length=10)
    # --> Here we are going to add the posts, but only with the related name 'posts', on the Post Model since it's a one to many relationship
    # --> The same thing goes for liked_posts
    # This sets the followers
    followers = models.ManyToManyField(to='self', related_name='following', blank=True)
    # This sets the following field
    following = models.ManyToManyField(to='self', related_name='user_following', symmetrical=False, blank=True)

    def __str__(self):
        return f'ID: {self.id} | Username: {self.user.username}'
