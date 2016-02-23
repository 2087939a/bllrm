from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import sys
import os
import urllib
from keys import YOUTUBE_API_KEY, BOILER_ROOM_CHANNELID



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
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s" % search_result["id"]["videoId"])
    
    return videos

videos = search_by_keyword()

print videos

print " -------------------------- "

def search_video_stats(v):

    search_response = youtube.search().list(
    part="statistics, snippet",
    videoId = v,
    
    
    ).execute()
    return search_response.get("items", [])

def parse_videos(videos):
    vs = []
    for vid in videos:
        list.append(search_video_stats(vid))
    return list
	# Create your views here.


# parse_videos(videos)
search_response = youtube.videos().list(
part="statistics,snippet",
id="vy-k0FopsmY",
fields = "items(statistics(viewCount), snippet(title,publishedAt), id)"
).execute()

print search_response.get("items" , [])[0]["id"]

print search_response.get("items" , [])

# https://developers.google.com/apis-explorer/#p/youtube/v3/youtube.videos.list?
# part=statistics%252C+snippet&
# id=vy-k0FopsmY&
# fields=items(statistics%252C+snippet(publishedAt%252Ctitle%252Cthumbnails(default(url))))&
# _h=1&

def index(request):

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "I am bold font from the context"}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    return render(request, 'index.html')

	
	
