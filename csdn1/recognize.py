#!/usr/bin/env python
# encoding: utf-8

import cv2
import string

def load_dataset(dataset):
    for j in string.digits:
        ch_images = []
        for k in range(6):
            image_file = 'dataset/%s%s.png' %(j,k)
            ch_images.append(cv2.imread(image_file,0))
        dataset[j] = ch_images

    return dataset

def count_distance(img1,img2):
    #assert img1.shape == img2.shape
    height = min(img1.shape[0],img2.shape[0])
    width = min(img1.shape[1],img2.shape[1])

    distance = 0
    for i in range(width):
        for j in range(height):
            if img1[j,i] != img2[j,i]:
                distance += 1

    return distance

def knn_classify(image,dataset,k):
    distance = []
    class_count = {}

    for key,value in dataset.items():
        for v in value:
            d = count_distance(image,v)
            distance.append((d,key))
    sorted_distance = sorted(distance)

    for i in range(k):
        vote_labels = sorted_distance[i][1]
        class_count[vote_labels] = class_count.get(vote_labels, 0) + 1
            
    max_count = 0
    max_label = -1
    for key,value in class_count.items():
        if value > max_count:
            max_count = value
            max_label = key

    return max_label


def split_image(image_name,col_range):
    image = cv2.imread(image_name,0)
    ret,image = cv2.threshold(image,180,255,cv2.THRESH_BINARY)
    height,width = image.shape
    #get part image by image[y1:y2,x1:x2]
    new_image = image[0:height,col_range[0]:col_range[1]]

    return new_image

def split(image_name):
    images = []

    images.append(split_image(image_name,(5,5+8)))
    images.append(split_image(image_name,(14,14+8)))
    images.append(split_image(image_name,(23,23+8)))
    images.append(split_image(image_name,(32,32+8)))

    return images

def recognize(img_file,dataset):
    images = split(img_file)
    code = []
    for image in images:
        c = knn_classify(image,dataset,5)
        code.append(str(c))
    return ''.join(code)

def main():
    dataset = {}
    load_dataset(dataset)
    for i in range(1,5):
        code = recognize('test%s.png'%i,dataset)
        print code

if __name__ == '__main__':
    main()
