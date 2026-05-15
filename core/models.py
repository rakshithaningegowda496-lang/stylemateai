import os, uuid
from django.db import models


def wardrobe_upload_path(instance, filename):
    ext  = os.path.splitext(filename)[1].lower()
    name = f"{uuid.uuid4().hex}{ext}"
    return f"wardrobe/{instance.category}/user_1/{name}"


class Profile(models.Model):
    name      = models.CharField(max_length=100, default="User")
    skin_tone = models.CharField(max_length=50)
    skin_type = models.CharField(max_length=50)
    body_type = models.CharField(max_length=50)
    gender    = models.CharField(max_length=50)
    location  = models.CharField(max_length=200, blank=True, null=True)


class UserProfile(models.Model):
    skin_tone = models.CharField(max_length=50)
    skin_type = models.CharField(max_length=50)
    body_type = models.CharField(max_length=50)
    gender    = models.CharField(max_length=50)
    location  = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.gender


class WardrobeItem(models.Model):
    name       = models.CharField(max_length=200)
    category   = models.CharField(max_length=100)
    style_type = models.CharField(max_length=50, default='casual')
    color_name = models.CharField(max_length=60, default='')
    color_hex  = models.CharField(max_length=7,  default='#000000')
    image      = models.ImageField(upload_to=wardrobe_upload_path, null=True, blank=True)
    color      = models.CharField(max_length=100, default='')
    fabric     = models.CharField(max_length=100, default='')
    occasion   = models.CharField(max_length=100, default='')
    season     = models.CharField(max_length=50,  default='')
    added_on   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category})"


class WeatherLog(models.Model):
    profile     = models.ForeignKey(Profile, on_delete=models.CASCADE)
    location    = models.CharField(max_length=100)
    temperature = models.FloatField()
    condition   = models.CharField(max_length=100)
    humidity    = models.FloatField()
    wind_speed  = models.FloatField()
    logged_at   = models.DateTimeField(auto_now_add=True)


class OutfitHistory(models.Model):
    profile     = models.ForeignKey(Profile, on_delete=models.CASCADE)
    occasion    = models.CharField(max_length=100)
    profession  = models.CharField(max_length=100, blank=True)
    mood        = models.CharField(max_length=100)
    colors_used = models.CharField(max_length=200)
    outfit_json = models.TextField()
    location    = models.CharField(max_length=100, blank=True)
    temperature = models.FloatField(null=True)
    condition   = models.CharField(max_length=100, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
def wardrobe_upload_path(instance, filename):
    import os, uuid
    ext  = os.path.splitext(filename)[1].lower()
    name = f"{uuid.uuid4().hex}{ext}"
    folder = f"wardrobe/{instance.category}/user_1"
    
    # Create folder if it doesn't exist
    full_folder = os.path.join(settings.MEDIA_ROOT, folder)
    os.makedirs(full_folder, exist_ok=True)
    
    return f"{folder}/{name}"