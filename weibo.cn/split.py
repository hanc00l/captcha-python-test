#!/usr/bin/env python
#-*- coding:utf-8 -*-

import cv2
import numpy as np
import uuid
import os

def is_black_line(image,x,y):
    if min(image[y,x,0],image[y,x,1],image[y,x,2]) < 12:
        return True
    else:
        return False

def is_black_pix(image,x,y):
    b = image[y,x,0]
    g = image[y,x,1]
    r = image[y,x,2]

    avg = (int(b)+int(g)+int(r))/3
    if r <244 and abs(avg-b) <4 and abs(avg-g) <4 and abs(avg-4) <4 :
        return True
    else:
        return False

def is_backgroud(image,x,y):
    if image[y,x] > 160:
        return True
    else:
        return False

def find_next_line_pos(image,p):
    height,width = image.shape[:2]
    next_pos = []
    if p['x'] >= width -1 :
        return []

    if is_black_line(image,p['x']+1,p['y']):
        next_pos.append({'x':p['x']+1,'y':p['y']}) 
    if p['y'] > 0 and is_black_line(image,p['x']+1,p['y']-1):
        next_pos.append({'x':p['x']+1,'y':p['y']-1}) 
    if p['y'] < height - 1 and is_black_line(image,p['x']+1,p['y']+1):
        next_pos.append({'x':p['x']+1,'y':p['y']+1}) 
    
    return next_pos

def find_line_path(image,path,p):
    height,width = image.shape[:2]
    if p['x'] >= width -1:
        return True
    next_pos = find_next_line_pos(image,p)
    if len(next_pos) == 0 :
        return False
    for np in next_pos:
        result = find_line_path(image,path,np)
        if result is True:
            path.append(np)
            return True

    return False

def find_first_pos_of_line(image):
    pos = []
    height,width = image.shape[:2]
    for y in range(height):
        if is_black_line(image,0,y):
            pos.append({'x':0,'y':y})
   
    return pos

def get_pix_gray_from_rgb(image,p):
    b = image[p['y'],p['x'],0]
    g = image[p['y'],p['x'],1]
    r = image[p['y'],p['x'],2]
    gray = r*0.299 + g*0.587 + b*0.114

    return int(gray)

def clear_horizotal_line_noise(image):
    first_pos = find_first_pos_of_line(image)
    if len(first_pos) == 0:
        return
    height,width = image.shape[:2]
    for pos in first_pos:
        path = []
        find_line_path(image,path,pos)
        if len(path) > 0:
            for p in path:
                if p['y'] == 0:
                    image[p['y'],p['x']] = image[p['y']+1,p['x']]
                elif p['y'] == height -1:
                    image[p['y'],p['x']] = image[p['y']-1,p['x']]
                else:
                    gray_top = get_pix_gray_from_rgb(image,{'x':p['x'],'y':p['y']-1})
                    gray_bottom = get_pix_gray_from_rgb(image,{'x':p['x'],'y':p['y']+1})
                    if gray_top >= gray_bottom:
                        image[p['y'],p['x']] = image[p['y']-1,p['x']]
                    else:
                         image[p['y'],p['x']] = image[p['y']+1,p['x']]
            break

def clear_pix_noise(image):
    height,width = image.shape[:2]
    for y in range(height):
        for x in range(width):
            white_color_num = 0
            if image[y,x] <=20 :
                if x > 0 and is_backgroud(image,x-1,y):
                    white_color_num += 1
                if x < width - 1 and is_backgroud(image,x+1,y):
                    white_color_num += 1
                if y > 0 and is_backgroud(image,x,y-1):
                    white_color_num += 1
                if y < height -1 and is_backgroud(image,x,y+1):
                    white_color_num += 1
 
                if white_color_num >= 2:
                    image[y,x] = 255
 
def clear_pix_noise_by_median_blue(image,p):
    gray_color = []
    for k in range(-1,2):
        for j in range(-1,2):
            gray_color.append(image[p['y']+k,p['x']+j])

    sorted_gray_color=sorted(gray_color)
    image[p['y'],p['x']] = sorted_gray_color[4]

def clear_noise(image):
    clear_horizotal_line_noise(image)
    clear_color(image)

    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    clear_pix_noise(image)
    ret, image = cv2.threshold(image,127,255,cv2.THRESH_BINARY)#+cv2.THRESH_OTSU)

    return image

def clear_color(image):
    height,width = image.shape[:2]
    for y in range(height):
        for x in range(width):
            if is_black_pix(image,x,y):
                image[y,x,0] = 20
                image[y,x,1] = 20
                image[y,x,2] = 20


def get_row_rect1(image):
    height,width = image.shape[:2]
    h = [0,]*height
    for y in range(height):
        for x in range(width):
            s = image[y,x] 
            if s < 12:
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

def get_row_rect(image):
    height,width = image.shape[:2]
    h = [0,]*height
 
    for y in range(height):
        for x in range(width):
            s = image[y,x] 
            if s < 12:
                h[y] += 1
    start_line = 0
    end_line = height -1

    for i in range(len(h)):
        if h[i] > 0:
            start_line = i
            break

    for i in range(len(h)):
        if h[height-1-i] > 0:
            end_line = height-1-i
            break

    return (start_line,end_line)

def get_col_rect(image):
    height,width = image.shape[:2]
    h = [0]*width
    for x in range(width):
        for y in range(1,height-1):
            s = image[y,x] 
            if s < 12:
                h[x] += 1
    col_rect = []
    in_line = False
    start_line = 0
    #####
    blank_distance = 1
    col_distance = 8
    ####
    for i in range(len(h)):
        if not in_line and h[i]>=blank_distance:
            in_line = True
            start_line = i
        elif in_line and h[i]<blank_distance and i-start_line > col_distance:
            rect = (start_line,i)
            col_rect.append(rect)
            in_line = False
            start_line = 0

    return col_rect

def get_block_image(image,col_rect):
    col_image = image[0:image.shape[0],col_rect[0]:col_rect[1]]
    #row_rect = (0,image.shape[0])
    row_rect = get_row_rect(col_image)
    #print row_rect
    if row_rect[1] != 0:
        block_image = image[row_rect[0]:row_rect[1],col_rect[0]:col_rect[1]]
    else:
        block_image = None
    return  block_image

def center_img(filename,height,width):
    img_org = cv2.imread(filename,0)
    img_new = np.zeros((height,width))
    img_new[...] = 255

    height_img_org,width_img_org = img_org.shape[:2]
    if height_img_org < height:
        y = (height - height_img_org) / 2
        yt = height_img_org
    else:
        y = 0
        yt = height
    if width_img_org < width:
        x = (width - width_img_org) / 2
        xt = width_img_org
    else:
        x = 0
        xt = width
    img_new[y:y+yt,x:x+xt] = img_org[0:yt,0:xt]
    cv2.imwrite(filename,img_new)

def split(filename,image_height,image_width):
    image =cv2.imread(filename)

    image = clear_noise(image)   
    col_rect = get_col_rect(image)
    #print col_rect
    for cols in col_rect:
        if cols[1] - cols[0] < 5:
            continue
        block_image = get_block_image(image,cols)
        if block_image is not None:
            new_image_filename = 'letters/'+str(uuid.uuid4())+'.png'
            cv2.imwrite(new_image_filename,block_image) 
            center_img(new_image_filename,image_height,image_width)  

def split_one_file(filename,image_height=20,image_width=20):
    image =cv2.imread(filename)

    image = clear_noise(image)   
    cv2.imwrite('/tmp/%s'%filename,image)   
    col_rect = get_col_rect(image)
    #print col_rect
    index = 1
    filenames = []
    for cols in col_rect:
        if cols[1] - cols[0] < 5:
            continue
        block_image = get_block_image(image,cols)
        if block_image is not None:
            new_image_filename = '/tmp/tmp_img_%s.png' %index
            cv2.imwrite(new_image_filename,block_image) 
            center_img(new_image_filename,image_height,image_width)   

            filenames.append(new_image_filename)
            index += 1

    return filenames

def main():
    image_height,image_width = 20,20
    #for i in range(10):
    #    split('test%s.png'%i)
    for file in os.listdir('./downloader/captchas'):
        f = './downloader/captchas/%s'%file
        if os.path.isfile(f) and f.endswith('.png'):
            split(f,image_height,image_width)
    
    print 'done...'

if __name__ == '__main__':
    main()
