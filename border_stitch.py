import cv2
import os
import numpy as np
def stitche(image_type):
    white=[255,255,255]
    #if os.path.isfile('./0.'+image_type) :
        #print('Already stitch')
    for i,j,k in os.walk('.',topdown=True):
        root=i
        dirs=j
        files=k
    apage = 0
    for i in files:         #filter img that resolution less than 1,000,000 pixel(credit strip)
        if i .split('.')[1] == image_type:
            #for x,y,chanel in cv2.imread(i, 1).shape:
             #   if x*y >= 1000000:
                    apage+=1
    #print(len(files))
    print('page = '+str(apage))
    single_img = cv2.imread(r'001.jpg', 1)
    #w,h = single_img.size
    single_img = cv2.copyMakeBorder(single_img, 20, 40, 20, 40, cv2.BORDER_CONSTANT, None, value=white)
    h,w,chanel = single_img.shape
    lw=w
    lh=(h*apage)
    long_size = (lw,lh)
    #long_img = cv2.CreateImage((lw,lh),no_of_bits,channels) 
    long_img = np.zeros(shape=[lh, lw, 3], dtype=np.uint8)
    for i in range(apage):
        a=i
        i+=1
        ia=str(i).zfill(3)+'.jpg'
        imgd = cv2.imread(ia, 1)
        imgbd = cv2.copyMakeBorder(imgd, 20, 40, 20, 40, cv2.BORDER_CONSTANT, None, value=white)
        hd,wd = imgbd.shape[:2]
        if wd*hd != (w)*(h): print('hd,wd = ',hd,wd)
        phead=hd*a
        pbutt=hd*i
        print(phead-pbutt)
        print(phead,pbutt)
        long_img[phead:(phead+hd),0:wd] = imgbd
    cv2.imwrite('0.jpg',long_img)
#img[pip_h:pip_h+h1,pip_w:pip_w+w1] = resized_image