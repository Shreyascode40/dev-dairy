from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    bio = models.TextField(blank=True, default='')
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, default='')
    github = models.URLField(blank=True, default='')
    instagram = models.URLField(blank=True, default='')
    facebook = models.URLField(blank=True, default='')
    twitter = models.URLField(blank=True, default='')
    linkedin = models.URLField(blank=True, default='')
    website = models.URLField(blank=True, default='')

    def __str__(self):
        return self.name


