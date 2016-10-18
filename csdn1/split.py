#!/usr/bin/env python
# encoding: utf-8
import os
import uuid
import cv2

def split_image(image_name,col_range):
    filename = 'letters/'+str(uuid.uuid4())+'.png'
    image = cv2.imread(image_name,0)
    ret,image = cv2.threshold(image,180,255,cv2.THRESH_BINARY)
    height,width = image.shape
    #get part image by image[y1:y2,x1:x2]
    new_image = image[0:height,col_range[0]:col_range[1]]
    cv2.imwrite(filename,new_image)

def split(image_name):
    split_image(image_name,(5,5+8))
    split_image(image_name,(14,14+8))
    split_image(image_name,(23,23+8))
    split_image(image_name,(32,32+8))

def main():
    for filename in os.listdir('captchas'):
        current_file = 'captchas/' + filename
        if os.path.isfile(current_file):
            split(current_file)
            print 'split file:%s'%current_file

if __name__ == '__main__':
    main()
    print 'done...'
