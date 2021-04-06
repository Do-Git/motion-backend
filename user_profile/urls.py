from django.urls import path

from user_profile.views import ListCreateUserProfileView, RetrieveUpdateDeleteUserProfileView, GetAllFollowers, \
    GetAllFollowing, ToggleFollowUnfollowView, GetSingleUserProfileView, GetUpdateMeView

urlpatterns = [
    path('', ListCreateUserProfileView.as_view()),
    path('<int:pk>/', RetrieveUpdateDeleteUserProfileView.as_view()),
    path('followers/followers/', GetAllFollowers.as_view()),
    path('followers/following/', GetAllFollowing.as_view()),
    path('followers/toggle-follow/<int:pk>/', ToggleFollowUnfollowView.as_view()),
    path('users/<int:pk>/', GetSingleUserProfileView.as_view()),
    path('me/', GetUpdateMeView.as_view()),
]
