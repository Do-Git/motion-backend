#from django.contrib import admin
from django.urls import path
#from rest_framework_simplejwt import views as jwt_views

from post.views import ListCreatePostView, RetrieveUpdateDeletePostView, ToggleLikePostView, ShowLikedPostsView, \
    ShowPostsOfFollowing, ShowAllPostsOfGivenUserView, PostsOfFriendsView, SharedPostView
#from user_profile.views import ToggleFollowUnfollowView

urlpatterns = [
    path('', ListCreatePostView.as_view()),
    path('<int:pk>/', RetrieveUpdateDeletePostView.as_view()),
    path('toggle-like/<int:pk>/', ToggleLikePostView.as_view()),
    path('likes/', ShowLikedPostsView.as_view()),
    path('following/', ShowPostsOfFollowing.as_view()),
    path('user/<int:pk>/', ShowAllPostsOfGivenUserView.as_view()),
    path('friends/', PostsOfFriendsView.as_view()),
    path('share/<int:pk>/', SharedPostView.as_view()),

]
