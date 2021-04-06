from django.urls import path

from friend_request.views import SendFriendRequestView, ViewFriendRequestsView, AcceptDeleteFriendRequestView

urlpatterns = [
    path('send/user/<int:pk>/', SendFriendRequestView.as_view()),
    path('view/', ViewFriendRequestsView.as_view()),
    path('accept-delete/<int:pk>/', AcceptDeleteFriendRequestView.as_view()),
]
