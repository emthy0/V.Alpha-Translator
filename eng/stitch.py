
from PIL import Image
import os
def stitche(image_type):
    if os.path.isfile('./0.'+image_type) :
        print('Already stitch')
    for i,j,k in os.walk('.',topdown=True):
        root=i
        dirs=j
        files=k
    apage = 0
    for i in files:
        if i .split('.')[1] == image_type:
            apage+=1
    #print(len(files))
    print('page = '+str(apage))
    Image.open('001.'+image_type).convert('RGB').save('001.jpg')
    single_img = Image.open('001.jpg')
    w,h = single_img.size
    lw=w+20
    lh=((h+10)*apage)+10
    long_size = (lw,lh)
    long_img = Image.new(mode='RGB',size=long_size,color=(255,255,255))
    for i in range(apage):
        i+=1
        ia=str(i).zfill(3)
        Image.open(ia+'.'+image_type).convert('RGB').save(ia+'.jpg')
        imgd =Image.open(ia+'.jpg')
        wd,hd = imgd.size
        #if (wd*hd)>=1000000 : img = imgd
        long_img.paste(imgd, (10,(10+(h*i))) )
    long_img.save('0.jpg')