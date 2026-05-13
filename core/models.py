from django.db import models

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    age = models.IntegerField()
    height = models.FloatField()

    image = models.ImageField(upload_to='profiles/')

    body_type = models.CharField(max_length=50, blank=True)
    skin_tone = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Outfit(models.Model):
    occasion = models.CharField(max_length=50)
    mood = models.CharField(max_length=50)
    recommendation = models.TextField()
class Profile(models.Model):
    name      = models.CharField(max_length=100, default="User")
    skin_tone = models.CharField(max_length=50)
    skin_type = models.CharField(max_length=50)
    body_type = models.CharField(max_length=50)
    gender    = models.CharField(max_length=50)
    location  = models.CharField(max_length=100)

class UserProfile(models.Model):
    skin_tone = models.CharField(max_length=50)
    skin_type = models.CharField(max_length=50)
    body_type = models.CharField(max_length=50)
    gender    = models.CharField(max_length=50)
    location  = models.CharField(max_length=100)
    def __str__(self):
        return self.gender

class Outfit(models.Model):
    occasion       = models.CharField(max_length=50)
    mood           = models.CharField(max_length=50)
    recommendation = models.TextField()

# ── NEW: User's own wardrobe items ──────────────
class WardrobeItem(models.Model):
    profile    = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    name       = models.CharField(max_length=200)
    color      = models.CharField(max_length=100)
    fabric     = models.CharField(max_length=100)
    occasion   = models.CharField(max_length=100)
    season     = models.CharField(max_length=50)
    category   = models.CharField(max_length=100)
    added_on   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.color})"

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
