import os
import sys
import urllib.request, urllib.error, urllib.parse,http.cookiejar
from bs4 import BeautifulSoup
import re
from urllib import request
import urllib
site=input()
# hdr = {'User-Agent' : "Magic Browser"}
#def src_download(site):  
os.chdir('./src/jpn/Jichou-shinai-motoyuusha/92')
site='https://lhscan.net/read-jichou-shinai-motoyuusha-no-tsuyokute-tanoshii-new-game-raw-chapter-92.html'
hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

#site = "https://lhscan.net/read-the-reincarnation-magician-of-the-inferior-eyes-raw-chapter-10.html"
hdr['Referer'] = site
req = urllib.request.Request(site, headers=hdr)
html = urllib.request.urlopen(req)
print('got html')
bs = BeautifulSoup(html, 'html.parser')
images = bs.find_all('img', {'data-src':re.compile('.jpeg')})
print('get image')
print(images)
i = 0
for image in images:
       print('start loop')
       f = open('./' + str(i.zfill(3)) + '.jpg','wb')
       req2 = urllib.request.Request(url=image['data-src'], headers=hdr)
       print((image['data-src']+'\n'))
       f.write(request.urlopen(req2).read())
       f.close()
       i += 1
       print('downloaded',i,'\n')
