from django.db import models

class FavoriteSong(models.Model):
    track_name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    popularity = models.IntegerField()

    def __str__(self):
        return self.track_name