
import re
import urllib2
import sys
import time
 
def crawl(url):
    if 'http' not in url:
        url = 'http://' + url
        
    sTUBE = ''
    cPL = ''
    amp = 0
    final_url = []
     
    if 'list=' in url:
        eq = url.rfind('=') + 1
        cPL = url[eq:]
             
    else:
        print('Incorrect Playlist.')
        exit(1)
     
    try:
        yTUBE = urllib2.urlopen(url).read()
        sTUBE = str(yTUBE)
    except urllib2.URLError as e:
        print(e.reason)
     
    tmp_mat = re.compile(r'watch\?v=\S+?list=' + cPL)
    mat = re.findall(tmp_mat, sTUBE)
 
    if mat:
           
        for PL in mat:
            yPL = str(PL)
            
            if '&' in yPL:
                yPL_amp = yPL.index('&')
            final_url.append(yPL[:yPL_amp].split('=')[1])
 
        all_url = list(set(final_url))
 

        return all_url
           
        
    else:
        print('No videos found.')
        exit(1)



videoList = crawl("https://www.youtube.com/watch?v=CevxZvSJLk8&list=PLWRJVI4Oj4IaYIWIpFlnRJ_v_fIaIl6Ey")
c = 0
for url in videoList:
    
    print c
    c += 1
    print (url)
    