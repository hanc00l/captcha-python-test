#!/usr/bin/env python
# encoding: utf-8

import cv2
import string

import split

def load_dataset(dataset):
    for j in string.digits:
        ch_images = []
        for k in range(5):
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

def split_image(filename):
    block_images = []

    image = split.clean_bg(filename)
    col_rect = split.get_col_rect(image)
    #print col_rect
    for cols in col_rect:
        block_image = split.get_block_image(image,cols)
        if block_image is not None:
            block_images.append(block_image)
            
    return block_images

def recognize(img_file,dataset):
    block_images = split_image(img_file)
    code = []
    for image  in block_images:
        c = knn_classify(image,dataset,4)
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
