from django.db import models
from django.contrib.auth.models import User



class Album(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=250)
    logo = models.FileField(max_length=1000)
    artist = models.CharField(max_length=250)

    def __str__(self):
        return self.title

    def songs(self):
        return self.song_set.all()


class Song(models.Model):
    album = models.ForeignKey(Album,on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    audio_file = models.FileField()

    def __str__(self):
        return self.title