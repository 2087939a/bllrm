import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blrrm.settings')

import django
django.setup()


from app.models import Video
import re
import urllib2
import sys
import gdata.youtube
import gdata.youtube.service
#use google api v3


def GetAndPrintVideoFeed(uri):
	yt_service = gdata.youtube.service.YouTubeService()
	yt_service.ssl = True
	feed = yt_service.GetYouTubeVideoFeed(uri)
	for entry in feed.entry:
		PrintEntryDetails(entry) # full documentation for this function

	
uri = "https://gdata.youtube.com/feeds/api/videos?author=brtvofficial&orderby=viewCount&max-results=10&v=2"
	
GetAndPrintVideoFeed(uri)

def add_video(name, url, videoid):
	v = Video.objects.get_or_create(name = name)[0]
	v.videoid = videoid
	
	v.save()
	return v

# Start execution here!
#if __name__ == '__main__':
#    print "Starting VideoPop population script..."
#    populate()
