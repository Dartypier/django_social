from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .models import Post, Comment
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentForm
from django.http import JsonResponse
from django.shortcuts import redirect
from accounts.models import UserFollowing
from django.db.models import Q


##handles POST and GET
class CommentCreateView(View):
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post_id = request.POST.get("post_id")
            comment.save()
        return redirect(request.META.get("HTTP_REFERER"))


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "comment_delete.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_comment"] = CommentForm()
        return context

    def get_queryset(self):
        # Get the posts of the users that the current user is following
        followed_users = UserFollowing.objects.filter(
            user_id=self.request.user
        ).values_list("following_user_id", flat=True)

        # Filter the posts based on the followed users
        queryset = Post.objects.filter(
            Q(author__in=followed_users) | Q(author=self.request.user)
        )

        return queryset


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_comment"] = CommentForm()
        return context

    # auto-set author to current-user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ("body",)
    template_name = "post_edit.html"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "post_create.html"
    fields = ("body",)

    # auto-set author to current-user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def like_post(request, pk):
    post = Post.objects.get(pk=pk)
    user = request.user

    if post.likes.filter(id=user.id).exists():
        # User already liked the post, remove the like
        post.likes.remove(user)
        liked = False
    else:
        # User hasn't liked the post, add the like
        post.likes.add(user)
        liked = True

    # Pass the liked status and total likes count to the template
    data = {
        "liked": liked,
        "count": post.likes.count(),
        "user_has_liked": post.likes.filter(id=user.id).exists(),
    }

    # Return a JSON response with the updated like status
    return JsonResponse(data)
