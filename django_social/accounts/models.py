from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image


class CustomUser(AbstractUser):
    # presets (AbstractUser):
    # username
    # date_joined
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    bio = models.TextField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=False, null=False, unique=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    avatar = models.ImageField(
        upload_to="avatar", default="user_avatar.png", blank=False
    )

    # Image avatar crop by Pillow
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar:
            image = Image.open(self.avatar.path)

            # Calculate the aspect ratio of the image
            aspect_ratio = image.width / image.height

            # Determine the dimensions for cropping
            if aspect_ratio > 1:
                # Landscape orientation
                new_width = image.height
                new_height = image.height
            else:
                # Portrait or square orientation
                new_width = image.width
                new_height = image.width

            # Calculate the coordinates for cropping
            left = (image.width - new_width) // 2
            top = (image.height - new_height) // 2
            right = left + new_width
            bottom = top + new_height

            # Crop the image
            cropped_image = image.crop((left, top, right, bottom))

            # Resize the cropped image to the desired size
            cropped_image = cropped_image.resize((600, 600), Image.ANTIALIAS)

            # Save the cropped and resized image back to the avatar field
            cropped_image.save(self.avatar.path)


# follow/unfollow model
class UserFollowing(models.Model):
    user_id = models.ForeignKey(
        CustomUser, related_name="following", on_delete=models.CASCADE
    )
    following_user_id = models.ForeignKey(
        CustomUser, related_name="followers", on_delete=models.CASCADE
    )
