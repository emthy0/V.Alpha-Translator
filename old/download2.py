'''
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
'''
import os
import urllib.request, urllib.error, urllib.parse,http.cookiejar
from bs4 import BeautifulSoup
import re



                    ################################################
                    #                                              #
                    #                                              #
                    # If get lhscan return forbiden try open site  #
                    # with browser and try again                   #
                    #                                              #
                    #                                              #
                    ################################################

#site = "https://lhscan.net/read-the-reincarnation-magician-of-the-inferior-eyes-raw-chapter-10.html"
def src_download(site):
    hdr={'User-Agent' : "Magic Browser"}
    req = urllib.request.Request(site, headers=hdr)
    print('url-get1')
    html = urllib.request.urlopen(req)
    print('url-get2')
    print(html)
    bs = BeautifulSoup(html, 'html.parser')
    images = bs.find_all('img', {'data-src':re.compile('.jpeg')})
    print(images)
    count=1
    print('url-get')
    for image in images: 
        refresher = urllib.request.URLopener()
        refresher.addheader('User-Agent',"Magic Browser")
        refresher.addheader('Referer',site)
        print((image['data-src']+'\n'))
        pagename=str(count).zfill(3)
        refresher.retrieve(image['data-src'],pagename)
        count+=1
os.chdir('./src/jpn/Jichou-shinai-motoyuusha/92')
site="https://lhscan.net/read-jichou-shinai-motoyuusha-no-tsuyokute-tanoshii-new-game-raw-chapter-92.html"        
src_download(site)
