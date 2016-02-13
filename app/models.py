from django.db import models

# Create your models here.
class Video(models.Model):
	fulltitle = models.CharField(max_length=128)
	videoid = models.CharField(max_length=128)
	views = models.IntegerField(default = None)
	date_uploaded = models.DateTimeField(default = None)
	location = models.CharField(max_length = 128, default = None)  #taken from string split of fulltitle
	artist = models.CharField(max_length = 128, default = None)    #taken from string split of fulltitle
	#most_asked_song = models.CharField(max_length = 256) as '%d:%d:%d'
