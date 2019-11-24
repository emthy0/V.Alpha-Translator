
from PIL import Image
import os
import cv2
def stitche(image_type):
    #if os.path.isfile('./0.jpg') :
    #    print('Already stitch')
    try: os.remove('0.jpg')
    except FileNotFoundError:print('')

    for i,j,k in os.walk('.',topdown=True):
        root=i
        dirs=j
        files=k
    apage = 0
    for i in files:
        if i .split('.')[1] == image_type:
            apage+=1
    #print(len(files))
    holder = 0
    while holder == 0:
        if image_type != 'jpg':
            for j in range(apage):
                j+=1
                ji=str(j).zfill(3)
                jor = str(j)+image_type
                jj = ji+'.jpg'
                img = cv2.imread(jor)
                cv2.imwrite(jj, img)
            image_type='jpg'              
                

        elif image_type == 'jpg':
            print('page = '+str(apage))
            single_img = Image.open('001.jpg')
            w,h = single_img.size
            lw=w+20
            lh=((h+10)*apage)+10
            long_size = (lw,lh)
            long_img = Image.new(mode='RGB',size=long_size,color=(255,255,255))
            for i in range(apage):
                i+=1
                ia=str(i).zfill(3)
                imgd = Image.open(ia+'.jpg')
                wd,hd = imgd.size
                #if (wd*hd)>=1000000 : img = imgd
                long_img.paste(imgd, (10,(10+(h*i))) )
            #rgb_im = im.convert('RGB')
            long_img.save('0.jpg')
            holder = 1