from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    bio = models.TextField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=False, null=False)
    age = models.PositiveIntegerField(null=True, blank=True)
    avatar = models.ImageField(
        upload_to="avatar", default="user_avatar.png", blank=True
    )
    follows = models.ManyToManyField(
        "self", blank=True, symmetrical=False, related_name="followers"
    )

    # presets:
    # username
    # date_joined

    ##Slug for using username instead of pk in urls

    def __str__(self):
        return self.username
