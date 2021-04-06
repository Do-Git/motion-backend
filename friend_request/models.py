
from django.db import models

# Create your models here.
from user_profile.models import UserProfile



class FriendRequest(models.Model):
    # This sets the field to see whether the request was accepted or not
    accepted = models.BooleanField(default=False)
    # This sets the field to see who received the request
    received_by = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='received_friend_requests')
    # This sets the field to see who sent the request
    sent_by = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='sent_friend_requests')

    def __str__(self):
        return f'ID: {self.id} | Receiver: {self.received_by.user.username} | Sent by: {self.sent_by.user.username}'