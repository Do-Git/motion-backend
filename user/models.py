from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # This forces users to login with their email instead of their username
    USERNAME_FIELD = 'email'
    # This makes the username required when creating a new superuser
    REQUIRED_FIELDS = ['username']
    # This overwrites the default behavior for this field. Now the email is required when signing up.
    email = models.EmailField(unique=True, blank=False)

    def __str__(self):
        return f'{self.id}: {self.email}'