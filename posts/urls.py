from django.urls import path, include
from .views import (
    PostListView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    PostCreateView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="home"),
    path("post/<str:author>/<int:pk>", PostDetailView.as_view(), name="post_detail"),
    path("post/<str:author>/<int:pk>/edit", PostUpdateView.as_view(), name="post_edit"),
    path(
        "post/<str:author>/<int:pk>/delete",
        PostDeleteView.as_view(),
        name="post_delete",
    ),
    path(
        "post/new",
        PostCreateView.as_view(),
        name="post_create",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("accounts.urls")),
]
