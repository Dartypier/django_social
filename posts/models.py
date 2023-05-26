from django.db import models
from django.urls import reverse
from django_quill.fields import QuillField
from accounts.models import CustomUser


class Post(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    body = QuillField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(CustomUser, blank=True, related_name="likes")

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return str(self.author) + "_" + str(self.pk)

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.author, self.pk])

    class Meta:
        db_table = "posts_post"
        ordering = ["-create_date"]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse("article_list")
