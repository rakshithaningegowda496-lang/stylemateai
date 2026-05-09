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