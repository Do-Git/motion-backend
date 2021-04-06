from rest_framework import serializers

from comment.serializers import SubCommentSerializer
from user_profile.serializers import UserProfileSerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    posted_by = UserProfileSerializer(read_only=True)
    liked_by = UserProfileSerializer(many=True, read_only=True)
    comments = SubCommentSerializer(many=True, read_only=True)
    shared_by = UserProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['posted_by', 'liked_by', 'comments', 'shared_by']
