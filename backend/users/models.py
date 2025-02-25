from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    

class YandexToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='yandex_token')
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)
    expires_in = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Yandex Token for {self.user.username}"
    
class GoogleToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='google_token')
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Google Token for {self.user.username}"

