from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, UpdateAPIView, \
    GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from user_profile.models import UserProfile
from user_profile.serializers import UserProfileSerializer
from user_profile.serializers import MeSerializer


class ListCreateUserProfileView(ListCreateAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

class IsOwnerOrViewer(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_profile = UserProfile.objects.get(user=request.user)
        if obj.user == user_profile or request.method == "GET":
            return True
        return False


class RetrieveUpdateDeleteUserProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfile
    queryset = UserProfile.objects.all()
    permission_classes = [IsOwnerOrViewer]


class GetAllFollowers(ListAPIView):
    serializer_class = UserProfileSerializer

    def list(self, request, *args, **kwargs):
        queryset = UserProfile.objects.filter(id__in=request.user.user_profile.followers.all())

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GetAllFollowing(ListAPIView):
    serializer_class = UserProfileSerializer

    def list(self, request, *args, **kwargs):
        queryset = UserProfile.objects.filter(id__in=request.user.user_profile.following.all())

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ToggleFollowUnfollowView(UpdateAPIView):
    serializer_class = UserProfileSerializer

    def update(self, request, *args, **kwargs):
        profile = UserProfile.objects.get(id=kwargs['pk'])
        users_following = profile.followers.values()

        if len(users_following) == 0:
            profile.followers.add(request.user.user_profile)
            return Response(self.get_serializer(profile).data)

        for user in users_following:
            if user['id'] == request.user.id:
                profile.followers.remove(request.user.user_profile)
                return Response(self.get_serializer(profile).data)

        profile.followers.add(request.user.user_profile)
        return Response(self.get_serializer(profile).data)


class AddRemoveFriends(UpdateAPIView):
    serializer_class = UserProfileSerializer

    def update(self, request, *args, **kwargs):
        profile = UserProfile.objects.get(id=kwargs['pk'])
        user_friends = profile.received_friend_requests.values().filter(accepted=True)


class GetSingleUserProfileView(ListAPIView):
    serializer_class = UserProfileSerializer

    def list(self, request, *args, **kwargs):
        queryset = UserProfile.objects.filter(id=kwargs['pk'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# class GetUpdateMeView(GenericAPIView):
#    serializer_class = MeSerializer
#    queryset = UserProfile.objects.all()

#    def get(self, request, *args, **kwargs):
#        return Response(self.get_serializer(request.user.user_profile).data)

#    def patch(self, request, *args, **kwargs):
#        serializer = self.get_serializer(request.user.user_profile, data=request.data, partial=True)
#        serializer.is_valid(raise_exception=True)
#      serializer.save()
#       return Response(serializer.data)

class GetUpdateMeView(RetrieveUpdateAPIView):
    serializer_class = MeSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [IsOwnerOrViewer]

    def get_object(self):
        return self.request.user.user_profile
