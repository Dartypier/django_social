from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, View
from .models import CustomUser, UserFollowing
from posts.models import Post


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        posts = Post.objects.filter(author=user)
        post_count = posts.count()
        followers_count = UserFollowing.objects.filter(following_user_id=user).count()
        following_count = UserFollowing.objects.filter(user_id=user).count()

        # Check if the current user is following the viewed user
        is_following = UserFollowing.objects.filter(
            user_id=self.request.user, following_user_id=user
        ).exists()

        context["posts"] = posts
        context["post_count"] = post_count
        context["followers_count"] = followers_count
        context["following_count"] = following_count
        context["is_following"] = is_following

        return context


class FollowToggleView(View):
    def post(self, request, pk, *args, **kwargs):
        user_to_follow = get_object_or_404(CustomUser, pk=pk)

        action = request.POST.get("action")

        if action == "follow":
            UserFollowing.objects.create(
                user_id=request.user, following_user_id=user_to_follow
            )
        elif action == "unfollow":
            UserFollowing.objects.filter(
                user_id=request.user, following_user_id=user_to_follow
            ).delete()

        prev_page = request.POST.get("prev_page", "/")
        return redirect(prev_page)
