from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .models import Post, Comment
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentForm
from django.http import JsonResponse


class CommentView:
    model = Comment

    def count_comments_for_article(self):
        pass


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_comment"] = CommentForm()
        return context


class PostDetailView(LoginRequiredMixin, DetailView, CommentView):
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
    success_url = reverse_lazy("user_profile")

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
