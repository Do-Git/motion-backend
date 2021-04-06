from rest_framework import serializers

from comment.models import Comment
from friend_request.serializers import FriendRequestSerializer
from user.serializers import UserSerializer
from user_profile.models import UserProfile
from post.models import Post
# from post.serializers import PostSerializer
from friend_request.models import FriendRequest


class NestedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content', 'posted_by']


class SubProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'first_name', 'last_name']


class NestedFriendRequestSerializer(serializers.ModelSerializer):
    # The Meta Class basically defines which model should be checked for the serializer.
    sent_by = SubProfileSerializer()
    received_by = SubProfileSerializer()

    class Meta:
        model = FriendRequest  # This defines the model that should be used. Don't forget to import it.
        fields = '__all__'  # This decides which fields of our chosen model should be used in the serializer to be displayed.


class UsernameProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['username']
        read_only_fields = ['username']


class NestedCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', ]


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    followers = SubProfileSerializer(read_only=True, many=True)
    following = SubProfileSerializer(read_only=True, many=True)
    sent_friend_requests = NestedFriendRequestSerializer(read_only=True, many=True)
    received_friend_requests = NestedFriendRequestSerializer(read_only=True, many=True)
    comments = NestedCommentSerializer(read_only=True, many=True)
    shared_posts = NestedPostSerializer(read_only=True, many=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'first_name', 'last_name', 'location', 'about', 'avatar', 'followers', 'following',
                  'comments', 'received_friend_requests', 'sent_friend_requests', 'shared_posts']
       # read_only_fields = ['user', 'followers', 'following', 'comments', 'shared_posts']


class MeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'avatar', 'user']
