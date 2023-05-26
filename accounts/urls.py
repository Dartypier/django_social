from django.urls import path, include
from .views import SignUpView, UserDetailView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user_profile"),
]
