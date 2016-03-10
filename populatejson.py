import json
import pandas as pd
import io, json
listOfIds = []
id = 0

addedList = list()

df = pd.read_csv('videos_sorted.csv')

columns = ['Artist','Location']

tempD = dict()
for c in columns:
	for name in df[c]:
		
		if name not in addedList:
				tempD = {'id':id,'name':name}
				addedList+=[name]
				listOfIds+=[tempD]
				id+=1
				
with open('ids.txt', 'w') as f:
	f.write(json.dumps(listOfIds))


# print listOfIds