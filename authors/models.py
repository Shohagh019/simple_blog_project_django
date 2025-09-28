# models.py
from django.db import models
from django.contrib.auth.models import User

def user_profile_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.user.username}_profile.{ext}"
    return f"user_profiles/{filename}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to=user_profile_image_path, default='default_avatar.png')
    phone_number = models.CharField(max_length=15, blank=True)
    birthdate = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

