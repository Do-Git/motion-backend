from rest_framework import serializers

from friend_request.models import FriendRequest
from user.serializers import UserSerializer
from user_profile.models import UserProfile


class NestedSubProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'first_name', 'last_name']


class FriendRequestSerializer(serializers.ModelSerializer):
    # The Meta Class basically defines which model should be checked for the serializer.
    sent_by = NestedSubProfileSerializer()
    received_by = NestedSubProfileSerializer()

    class Meta:
        model = FriendRequest # This defines the model that should be used. Don't forget to import it.
        fields = '__all__' # This decides which fields of our chosen model should be used in the serializer to be displayed.