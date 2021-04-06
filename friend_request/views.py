from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from friend_request.models import FriendRequest
from friend_request.serializers import FriendRequestSerializer
from user_profile.models import UserProfile


class SendFriendRequestView(GenericAPIView):
    serializer_class = FriendRequestSerializer

    def post(self, request, *args, **kwargs):
        receiver = UserProfile.objects.get(id=kwargs['pk'])
        friend_request = FriendRequest(accepted=False, received_by=receiver, sent_by=request.user.user_profile)
        friend_request.save()
        return Response({'status': 'Request sent'}, status=201)


class ViewFriendRequestsView(ListAPIView):
    serializer_class = FriendRequestSerializer

    def list(self, request, *args, **kwargs):
        queryset = FriendRequest.objects.filter(received_by=request.user.user_profile)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class IsInFriendRequest(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_profile = UserProfile.objects.get(user=request.user)
        if obj.received_by == user_profile or obj.sent_by == user_profile:
            return True
        return False

class AcceptDeleteFriendRequestView(GenericAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsInFriendRequest]

    def get(self, request, *args, **kwargs):
        friend_request = self.get_object()  # The get_object() function returns only ONE instance from the queryset. This will actually automatically check for the kwargs (which are found in the URL) and then use whatever is in the kwargs (so it would be an ID in this case) to filter out the correct instance.
        serializer = self.get_serializer(friend_request)  # This will serialize the data of the instance to turn it into usable python data.
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        friend_request = self.get_object()
        serializer = self.get_serializer(friend_request, data=request.data, partial=True)  # Add the "partial=True" to the serializer, to allow partial updates. This is the difference between PUT and PATCH.
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        friend_request = self.get_object()
        friend_request.delete()
        return Response('Deleted')