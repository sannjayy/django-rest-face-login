from django.db import models
from django.contrib.auth.models import AbstractUser
import os, uuid
from django.conf import settings

class User(AbstractUser):
    screen_lock_img = models.ImageField(upload_to='security_images', null=True, blank=True)

    @property
    def screen_lock_img_url(self):
        try:
            url = self.screen_lock_img.url.replace('/', '\\')[1:]
        except:
            url = None

        return url

class LoginAttempt(models.Model):
    username = models.CharField(max_length=50)
    image = models.ImageField(upload_to='uploaded_temp_images', blank=False, null=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.username


    @property
    def get_absolute_image_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.image.url)

        
    @property
    def image_url(self):
        try:
            url = self.image.url.replace('/', '\\')[1:]
        except:
            url = None

        return url

