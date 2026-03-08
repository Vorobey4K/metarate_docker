import os

from django.contrib.auth import get_user_model
from django.db import models

def user_directory_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f'users/{instance.user.username}_avatar{ext}'

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(
        upload_to=user_directory_path,
        null=True,
        blank=True,
    )

    @property
    def photo_exists(self):
        if self.photo and os.path.isfile(self.photo.path):
            return True
        return False