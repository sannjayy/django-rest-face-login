from django.db import models
from django.contrib.auth.models import AbstractUser
import os

class User(AbstractUser):
    screen_lock_img = models.ImageField(upload_to='security_images', null=True, blank=True)

    @property
    def image_filename(self):
        try:
            return os.path.basename(self.screen_lock_img.name)
        except:
            return None



class LoginAttempt(models.Model):
    username = models.CharField(max_length=50)
    image = models.ImageField(upload_to='uploaded_temp_images', blank=False, null=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.username

    @property
    def image_url(self):
        try:
            return os.path.basename(self.image.name)
        except:
            return None

