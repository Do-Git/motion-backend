from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.response import Response

from comment.models import Comment
from comment.serializers import CommentSerializer
from post.models import Post


class ListCreateCommentView(ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Post.objects.all()

    def create(self, request, *args, **kwargs):
        post = get_object_or_404(self.get_queryset(), id=kwargs['pk'])
        comment = Comment(content=request.data['content'], user_profile=request.user.user_profile, post=post)
        comment.save()
        return Response(self.get_serializer(comment).data)

    def list(self, request, *args, **kwargs):
        post = self.get_object()
        return Response(self.get_serializer(post.comments, many=True).data)