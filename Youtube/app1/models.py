from django.contrib.auth.models import User
from django.db import models

class Profil(models.Model):
    ism = models.CharField(max_length=50)
    bio = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.ism

class Video(models.Model):
    nom = models.CharField(max_length=50)
    video = models.URLField()
    korildi = models.PositiveIntegerField(default=0)
    vaqt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profil, on_delete=models.CASCADE, related_name='uservideos')

    def __str__(self):
        return self.nom

class Playlist(models.Model):
    nom = models.CharField(max_length=50)
    videos = models.ManyToManyField(Video, related_name='playlistvideos')
    user = models.ForeignKey(Profil, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom

class Comment(models.Model):
    matn = models.TextField()
    user = models.ForeignKey(Profil, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='videocomments')
    vaqt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.matn