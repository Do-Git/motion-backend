
from django.shortcuts import render

# Create your views here.
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, ListAPIView, \
    GenericAPIView
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from post.models import Post
from post.serializers import PostSerializer
from user_profile.models import UserProfile
from friend_request.models import FriendRequest


# from friend_request.serializers import FriendRequestSerializer

class ListCreatePostView(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    search_fields = ['content', ]
    filter_backends = (filters.SearchFilter,)

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user.user_profile)

class IsOwnerOrViewer(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_profile = UserProfile.objects.get(user=request.user)
        if obj.posted_by == user_profile or request.method == "GET":
            return True
        return False


class RetrieveUpdateDeletePostView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsOwnerOrViewer]


class ToggleLikePostView(UpdateAPIView):
    serializer_class = PostSerializer

    def update(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs['pk'])
        users_liked = post.liked_by.values()

        if len(users_liked) == 0:
            post.liked_by.add(request.user.user_profile)
            return Response(self.get_serializer(post).data)

        for user in users_liked:
            if user['id'] == request.user.id:
                post.liked_by.remove(request.user.user_profile)
                return Response(self.get_serializer(post).data)

        post.liked_by.add(request.user.user_profile)
        return Response(self.get_serializer(post).data)


class ShowLikedPostsView(ListAPIView):
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        queryset = Post.objects.filter(liked_by=request.user.id)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ShowPostsOfFollowing(ListAPIView):
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        queryset = Post.objects.filter(posted_by__in=request.user.user_profile.following.all())

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ShowAllPostsOfGivenUserView(ListAPIView):
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        queryset = Post.objects.filter(posted_by__id=kwargs['pk'])

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PostsOfFriendsView(GenericAPIView):
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        user_profile = request.user.user_profile
        friendship_requested = FriendRequest.objects.filter(sent_by=user_profile, accepted=True)
        friendship_received = FriendRequest.objects.filter(received_by=user_profile, accepted=True)
        friendship_user_profile = []
        for friendship in friendship_requested:
            friendship_user_profile.append(friendship.received_by)
        for friendship in friendship_received:
            friendship_user_profile.append(friendship.sent_by)
        posts = Post.objects.filter(posted_by__in=friendship_user_profile)
        return Response(self.get_serializer(posts, many=True).data)

class SharedPostView(UpdateAPIView):
    serializer_class = PostSerializer

    def update(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs['pk'])
        users_shared = post.shared_by.values()
        post.shared_by.add(request.user.user_profile)
        return Response(self.get_serializer(post).data)

