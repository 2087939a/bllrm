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





from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import sys
import os
import urllib
from app.keys import YOUTUBE_API_KEY, BOILER_ROOM_CHANNELID



# Set API_KEY to the "API key" value from the "Access" tab of the
# Google APIs Console http://code.google.com/apis/console#access
# Please ensure that you have enabled the YouTube Data API and Freebase API
# for your project.
API_KEY = YOUTUBE_API_KEY 
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
QUERY_TERM = ""

youtube = build(
YOUTUBE_API_SERVICE_NAME, 
YOUTUBE_API_VERSION, 
developerKey=API_KEY
)


def search_by_keyword():

    search_response = youtube.search().list(
    part="snippet",
    channelId = BOILER_ROOM_CHANNELID,
    order = "viewCount",
    maxResults=11
    ).execute()
    videos = []
    v = dict()
    titles = []
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s" % str(search_result["id"]["videoId"]))
            v[search_result["id"]["videoId"]] = search_result["snippet"]["title"]
            titles.append("%s" % search_result["snippet"]["title"])
    print v
    print titles
    return videos

videos = search_by_keyword()

print videos

print " -------------------------- "



def parse_videos(videos):
    d = dict()
    for vid in videos:
        d[vid] = get_stats(vid)
    return d
	# Create your views here.

def get_stats(videoId):
    # parse_videos(videos)
    search_response = youtube.videos().list(
    part="statistics,snippet",
    id=videoId,
    fields = "items(statistics(viewCount), snippet(title,publishedAt))"
    ).execute()
    return search_response.get("items" , [])[0]


print parse_videos(videos)
	

# https://developers.google.com/apis-explorer/#p/youtube/v3/youtube.videos.list?
# part=statistics%252C+snippet&
# id=vy-k0FopsmY&
# fields=items(statistics%252C+snippet(publishedAt%252Ctitle%252Cthumbnails(default(url))))&
# _h=1&


def add_video(name, url, videoid):
	v = Video.objects.get_or_create(name = name)[0]
	v.videoid = videoid
	
	v.save()
	return v

# Start execution here!
if __name__ == '__main__':
    print "Starting population script..."
    populate()
