#!/usr/bin/env python
# encoding: utf-8
import os
import uuid
import cv2
import numpy as np


def horizontal_image(image):
    height,width,dept = image.shape[:2]
    h = [0]*height
    for y in range(height):
        for x in range(width):
            s = image[y,x] #max(image[y,x][0],image[y,x][1],image[y,x][2])
            if s == 255:
                h[y] += 1
    new_image = np.zeros(image.shape,np.uint8)
    for y in range(height):
        cv2.line(new_image,(0,y),(h[y],y),255,1)
    cv2.imshow('hori_image',new_image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

def vertical_image(image):
    height,width,dept = image.shape[:2]
    h = [0]*width
    for x in range(width):
        for y in range(height):
            s = image[y,x]#max(image[y,x][0],image[y,x][1],image[y,x][2])
            if s == 255:
                h[x] += 1
    new_image = np.zeros(image.shape,np.uint8)
    for x in range(width):
        cv2.line(new_image,(x,0),(x,h[x]),255,1)
    cv2.imshow('vert_image',new_image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()


def get_row_rect(image):
    height,width = image.shape[:2]
    h = [0] * height
    for y in range(height):
        for x in range(width):
            s = image[y,x] #max(image[y,x][0],image[y,x][1],image[y,x][2])
            if s == 255:
                h[y] += 1
    in_line = False
    start_line = 0
    ####
    blank_distance = 1
    ####
    row_rect = (0,0)
    for i in range(len(h)):
        if not in_line and h[i]>=blank_distance:
            in_line = True
            start_line = i
        elif in_line and h[i]<blank_distance:
            row_rect = (start_line,i)
            break

    return row_rect

def get_col_rect(image):
    height,width = image.shape[:2]
    h = [0] * width
    for x in range(width):
        for y in range(height):
            s = image[y,x] #max(image[y,x][0],image[y,x][1],image[y,x][2])
            if s == 255:
                h[x] += 1
    col_rect = []
    in_line = False
    start_line = 0
    #####
    blank_distance = 1
    ####
    for i in range(len(h)):
        if not in_line and h[i]>=blank_distance:
            in_line = True
            start_line = i
        elif in_line and h[i]<blank_distance:
            rect = (start_line,i)
            col_rect.append(rect)
            in_line = False
            start_line = 0

    return col_rect

def get_block_image(image,col_rect):
    col_image = image[0:image.shape[0],col_rect[0]:col_rect[1]]
    row_rect = get_row_rect(col_image)
    #print row_rect
    if row_rect[1] != 0:
        block_image = image[row_rect[0]:row_rect[1],col_rect[0]:col_rect[1]]
    else:
        block_image = None
    return  block_image


def clean_bg(filename):
    image = cv2.imread(filename,0)
    new_image = np.zeros(image.shape, np.uint8)
    height,width= image.shape

    for i in range(height):
        for j in range(width):
            new_image[i,j] = image[i,j]#max(image[i,j][0],image[i,j][1],image[i,j][2])

    ret,new_image = cv2.threshold(new_image,180,255,cv2.THRESH_BINARY_INV)
    border_width = 2
    new_image = new_image[border_width:height-border_width,border_width:width-border_width]
    #cv2.imshow('invImage',new_image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return new_image

def split(filename):
    image = clean_bg(filename)
    col_rect = get_col_rect(image)
    #print col_rect
    for cols in col_rect:
        block_image = get_block_image(image,cols)
        if block_image is not None:
            new_image_filename = 'letters/'+str(uuid.uuid4())+'.png'
            cv2.imwrite(new_image_filename,block_image)   

def test():
    image = clean_bg('../4.png')
    #horizontal_image(image)
    #row_rect = get_row_rect(image)
    #print row_rect
    #vertical_image(image)
    col_rect = get_col_rect(image)
    print col_rect
    index = 0
    for cols in col_rect:
        block_image = get_block_image(image,cols)
        #col_image = image[0:image.shape[0],cols[0]:cols[1]]
        #cv2.imshow('col%s'%index,col_image)
        cv2.imshow('block%s'%index,block_image)
        index += 1
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    for filename in os.listdir('captchas'):
        current_file = 'captchas/' + filename
        if os.path.isfile(current_file):
            split(current_file)
            print 'split file:%s'%current_file   

if __name__ == '__main__':
    main()

