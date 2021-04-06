import random

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from user_profile.models import UserProfile
User = get_user_model()


def code_generator(length=5):
    numbers = '0123456789'
    return ''.join(random.choice(numbers) for _ in range(length))


class Registration(models.Model):
    code = models.CharField(max_length=6, default=code_generator)
    user = models.OneToOneField(to=UserProfile, on_delete=models.CASCADE, related_name='profile')
    code_used = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}: Profile from {self.user.username}'

    # @receiver(post_save, sender=User)
    # def create_registration_profile(sender, instance, **kwargs):
    #     profile, created = UserProfile.objects.get_or_create(user=instance)
    #     if created:
    #         profile.save()
