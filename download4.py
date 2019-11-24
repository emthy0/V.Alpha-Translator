import os,sys
import urllib.request, urllib.error, urllib.parse,http.cookiejar
from bs4 import BeautifulSoup
import re
import cloudscraper
from PIL import ImageFile
from progressbar import ProgressBar
'''
def getsizes(uri):
    # get file size *and* image size (None if not known)
    scraper = cloudscraper.create_scraper()
    size = scraper.get(site)

    if size: 
        size = int(size)
    p = ImageFile.Parser()
    while True:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return size, p.image.size
            break
    file.close()
    return(size, None)

def hook(count, block_size, total_size,pagename):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = min(int(count * block_size * 100 / total_size),100)
    sys.stdout.write("\r File's size =[%d%% %s], %d MB, %d KB/s, %d seconds passed" % (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()
'''


def reporthook(blocknum, blocksize, totalsize):
    readsofar = min(blocknum * blocksize ,totalsize)
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize: # near the end
            sys.stderr.write("\n")
    else: # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))


def src_download(site):
    print('Sending Request to site')
    scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
    html=scraper.get(site).content
    print('Inspecting URL')
    #print(html)  # => "<!DOCTYPE html><html><head>..."
    bs = BeautifulSoup(html, 'html.parser')
    #print('\n\n\n\n ----------------got html--------------\n\n\n\n')
    #print(bs.prettify())
    images = bs.find_all('img', {'class':re.compile('chapter-img')})
    #print(images)
    count=1
    print('Start Download Source Image')
    for image in images: 
        refresher = urllib.request.URLopener()
        refresher.addheader('User-Agent',"Magic Browser")
        refresher.addheader('Referer',site)
        imurl_type = (image['data-src']).split('.')
        img_type = imurl_type[len(imurl_type)-1]
        pagename=str(count).zfill(3)
        pagename=pagename+'.'+str(img_type)
        #print(getsizes(image['data-src']))
        asd='Downloading :'+pagename
        print(asd)
        refresher.retrieve(image['data-src'],pagename.rstrip('\n'))
        if img_type != 'jpg':
            os.system('mogrify -format jpg *.{}'.format(img_type))
        #print((image['data-src']+'\n'))
        count+=1


#os.chdir('./src/jpn/Jichou shinai motoyuusha no tsuyokute tanoshii new game/92')
#site="https://lhscan.net/read-sobiwaku-zero-no-saikyou-kenshi-demo-noroi-no-soubi-kawai-nara-9999-ko-tsuke-hodai-raw-chapter-1.html"        
#src_download(site)
'''
'''