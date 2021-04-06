from rest_framework import serializers

from user_profile.serializers import UserProfileSerializer
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user_profile']
        read_only_fields = ['user_profile']


class SubCommentSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user_profile']