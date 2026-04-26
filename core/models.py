from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=100, default="User")
    skin_tone = models.CharField(max_length=50)
    skin_type = models.CharField(max_length=50)
    body_type = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    location = models.CharField(max_length=100)


class Outfit(models.Model):
    occasion = models.CharField(max_length=50)
    mood = models.CharField(max_length=50)
    recommendation = models.TextField()