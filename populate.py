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


import csv

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import sys
import os
import urllib
from app.keys import YOUTUBE_API_KEY, BOILER_ROOM_CHANNELID
from youParse import crawl
import datetime

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




def formatTitle(title):
	stopwords = ['boiler', 'room', 'set', 'mix', 'takeovers', 'villa', 
				'takeover', 'young', 'turks', 'min', '90', '3.5', 
				'60', '35', '100', 'hour', 'red', 'bull', 
				'music' ,'academy' ,'rbma', 'x', 'minute', 'live', 'show', '50', 
				"ballantine's", 'by', 'in', '75', '55', '45' , '30', 'stay', 'true',
				'70', 'take-over','ray-ban', '80', 'IR', 'studios', '105', 'series',
				'broadcasts', '009', 'hip-hop', 'bridgesformusic.org', '40', '65', 'opening', 
				'concert', 'vans', '5th', 'birthday', 'daytime']
	titleList = title.split()
	locationList = []
	artist = []
	for word in titleList:
		i = 0
		
		if word.lower() in stopwords:
			i+=1
			locationList = titleList[len(artist):]
			
			break
		artist.append(word)
		i += 1
		
	otherstop = ['dj','at', 'the', '&', '-', '/', 'of', 'house', 'in', 'stereo']
	stopwords = stopwords+otherstop
	location = [w for w in locationList if w.lower() not in stopwords]
	format = []
	format.append(" ".join(artist))
	format.append(" ".join(location))
	return format

def search_by_keyword():

    search_response = youtube.search().list(
    part="snippet",
    channelId = BOILER_ROOM_CHANNELID,
    order = "viewCount",
    maxResults=50
    ).execute()
    videos = []
    v = dict()
    titles = []
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s" % str(search_result["id"]["videoId"]))
            v[search_result["id"]["videoId"]] = search_result["snippet"]["title"]
            titles.append("%s" % search_result["snippet"]["title"])

    return videos

videos = crawl("https://www.youtube.com/watch?v=vy-k0FopsmY&list=PUGBpxWJr9FNOcFYA5GkKrMg")


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

def createcsvfile(videoList):
    csvfile = open('videos.csv', 'wb')
    fieldnames = ['videoID', 'Artist','Location','Date', 'Title', 'viewCount', ]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    with open('videos.csv', 'wb') as csvfile:
        d = parse_videos(videoList)
        for vid in videoList:
            dateOfVid = d[vid]['snippet']['publishedAt']
            dateOfVid = dateOfVid.split('T')[0]
            dateOfVid = datetime.datetime.strptime(dateOfVid,'%Y-%m-%d').date()
            titleOfVid = d[vid]['snippet']['title'].encode('utf-8').strip()
            format = formatTitle(titleOfVid)
            location = format[1]

            artist = format[0]
            
            
            writer.writerow({'videoID': vid, 
			                 'Artist' : artist,
							 'Location' : location,
                             'Date': dateOfVid,
                             'Title' : titleOfVid,
                             'viewCount' : d[vid]['statistics']['viewCount'],
							
                            })





	

def populate():
    createcsvfile(videos)
	
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
