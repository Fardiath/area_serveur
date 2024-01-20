from django.db import models

# Create your models here.

class MaEntite(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.nom
    
    
class YoutubeVideo(models.Model):
    video_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail_url = models.URLField()

    def __str__(self):
        return self.title

MaEntite._meta.app_label = 'areact'