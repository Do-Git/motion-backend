# Generated by Django 3.0.3 on 2021-03-25 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
        ('post', '0003_auto_20210324_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='shared_by',
            field=models.ManyToManyField(blank=True, related_name='shared_posts', to='user_profile.UserProfile'),
        ),
    ]