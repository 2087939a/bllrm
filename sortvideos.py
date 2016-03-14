import pandas as pd
import csv

def sortVideos():
    df = pd.read_csv('videos.csv', sep = ';')
    df = df.sort_values('viewCount', ascending = False)
    df.to_csv('videos_sorted.csv', index=False, sep=';')
