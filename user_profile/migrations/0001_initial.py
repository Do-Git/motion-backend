# Generated by Django 3.0.3 on 2021-03-23 13:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import user_profile.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=100)),
                ('about', models.TextField(max_length=500)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=user_profile.models.user_directory_path)),
                ('phone', models.CharField(max_length=10, unique=True)),
                ('followers', models.ManyToManyField(blank=True, related_name='_userprofile_followers_+', to='user_profile.UserProfile')),
                ('following', models.ManyToManyField(blank=True, related_name='user_following', to='user_profile.UserProfile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]