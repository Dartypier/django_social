from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .models import CustomUser
from posts.models import Post, Comment


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class UserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "user_detail.html"

    # get context of posts and comments
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        posts = Post.objects.filter(author=user)
        post_count = posts.count()
        followers_count = user.followers.all().count()
        following_count = user.follows.all().count()
        context["posts"] = posts
        context["post_count"] = post_count
        context["followers_count"] = followers_count
        context["following_count"] = following_count
        return context

    # no need because pk is already specified in URL
    # def get_object(self, queryset=None):
    #     obj = super().get_object(queryset=queryset)
    #     return obj
