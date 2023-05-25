from django.db import models
from django.urls import reverse
from django_quill.fields import QuillField


class Post(models.Model):
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
    )
    body = QuillField()
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.author) + "_" + str(self.pk)

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.author, self.pk])

    class Meta:
        db_table = "posts_post"
        db_table_comment = "This table contains user related posts"
        ordering = ["-create_date"]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse("article_list")
