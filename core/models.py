from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=100, default="User")
    skin_tone = models.CharField(max_length=50)
    skin_type = models.CharField(max_length=50)
    body_type = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    location = models.CharField(max_length=100)


<<<<<<< HEAD
class UserProfile(models.Model):
    skin_tone = models.CharField(max_length=50)
    skin_type = models.CharField(max_length=50)
    body_type = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    location = models.CharField(max_length=100)

def __str__(self):
    return self.gender


=======
class Outfit(models.Model):
    occasion = models.CharField(max_length=50)
    mood = models.CharField(max_length=50)
    recommendation = models.TextField()
>>>>>>> 02e436f84cf7aeb21df953b9fc65d8b533f4d188
