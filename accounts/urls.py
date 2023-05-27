from django.urls import path, include
from .views import (
    SignUpView,
    UserDetailView,
    FollowToggleView,
    UserListView,
    ChangeUserProfile,
)

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user_profile"),
    path("user/<int:pk>/follow/", FollowToggleView.as_view(), name="follow_toggle"),
    path("users/", UserListView.as_view(), name="user_list"),
    path("user/edit", ChangeUserProfile.as_view(), name="user_change"),
]
