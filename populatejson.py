import json
import pandas as pd
import io, json
import csv




def populateJson():
	listOfIds = []
	id = 0

	addedList = list()
	videos = csv.DictReader(open("videos_sorted.csv"), delimiter = ';')
	df = pd.read_csv('videos_sorted.csv', sep = ';')



	tempD = dict()
	locationViews = dict()


	for row in videos:
		if row['Location'] not in locationViews.keys():
			locationViews[row['Location']] = 0
			locationViews[row['Location']] += int(row['viewCount'])
		elif row['Location'] in locationViews.keys():
			locationViews[row['Location']] += int(row['viewCount'])
		if row['Artist'] not in addedList:
				tempD = {'id':id,'name':row['Artist'], 'views':int(row['viewCount'])}
				addedList+=[row['Artist']]
				listOfIds+=[tempD]
				id+=1

		#elif row.artist in addedlist then add the viewcount to the artist's dict and location dict
		elif row['Artist'] in addedList:
			for d in listOfIds:
				if d['name']==row['Artist']:
					d['views'] += int(row['viewCount'])
				
	
	for location in df['Location']:
		if location not in addedList:
			tempD = {'id':id,'name':location, 'views':locationViews[location]}
			addedList+=[location]
			listOfIds+=[tempD]
			id+=1
	
	
	with open('ids.txt', 'w') as f:
		f.write(json.dumps(listOfIds))

	f.close()
	videos = csv.DictReader(open("videos_sorted.csv"), delimiter = ';')



	with open('ids.txt', 'r') as f:
		nodes = json.load(f)


	links = []
	names = []
	for row in videos:
		artist = row['Artist']
		location = row['Location']
		sourceArtistId = 0
		targetLocId = 0
		for node in nodes:
			if artist==node['name'].encode('utf-8'):
				sourceArtistId = node['id']
			elif location==node['name'].encode('utf-8'):
				targetLocId = node['id']
		names.append([artist,location])
		links.append({'source':sourceArtistId,'target':targetLocId})

	with open('links.txt', 'w') as f:
		f.write(json.dumps(links))

	f.close()


