from django.urls import path

from comment.views import ListCreateCommentView

urlpatterns = [
    path('post/<int:pk>/', ListCreateCommentView.as_view()),
]
