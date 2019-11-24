'''
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
'''
import os
import urllib3,cookielib
from bs4 import BeautifulSoup
import re



site = "https://lhscan.net/read-the-reincarnation-magician-of-the-inferior-eyes-raw-chapter-10.html"
req = urllib2.Request(site, headers={'User-Agent' : "Magic Browser"})
html = urllib2.urlopen(req)
bs = BeautifulSoup(html, 'html.parser')
images = bs.find_all('img', {'data-src':re.compile('.jpeg')})
for image in images: 
    print(image['data-src']+'\n')


