#!/usr/bin/env python
#-*- coding:utf-8 

import cv2
import os
import string
from svmutil import *

def get_feature(filename):
    image = cv2.imread(filename,0)
    height,width = image.shape[:2]
    assert height == 20
    assert width == 20
    result = []
    for y in range(0,height,2):
        for x in range(0,width,2):
            black_color = 0
            if image[y,x] < 127:
                black_color += 1
            if image[y,x+1] < 127:
                black_color += 1
            if image[y+1,x] < 127:
                black_color += 1
            if image[y+1,x+1] < 127:
                black_color += 1
            result.append(black_color)

    return result

def get_train_features(labels):
    results = []
    for l in labels:
        image_path = 'train/%s' %l
        features = []
        index = string.printable.find(l)
        for filename in os.listdir(image_path):
            f = '%s/%s'%(image_path,filename)
            if os.path.isfile(f) and f.endswith('.png'):
                feature_data = get_feature(f)
                feature_data_lines = []
                #data ->: 1:X 2:Y 3:Z ...
                for j,data in enumerate(feature_data):
                    feature_data_lines.append('%s:%s'%(j+1,data))
                #data ->: index 1:X 2:Y 3:Z ...
                features.append('%s %s'%(index,' '.join(feature_data_lines)))
        results.extend(features)
        
    return results

def _model_train(svm_feature_filename,svm_model_filename):
    y, x = svm_read_problem(svm_feature_filename)
    m = svm_train(y,x,'-c 4')
    svm_save_model(svm_model_filename,m)
    
def _model_test(svm_model_filename,svm_test_filename):
    yt, xt = svm_read_problem(svm_test_filename)
    model = svm_load_model(svm_model_filename)
    p_label, p_acc, p_val = svm_predict(yt, xt, model)
    
    return p_label
    
def _model_test_one(svm_model_filename,feature_data):
    model = svm_load_model(svm_model_filename)
    y = [-1,]
    x = [feature_data]

    p_label, p_acc, p_val = svm_predict(y, x, model)
    return p_label

def model_test_for_file(svm_model_filename,filename):
    feature_data = get_feature(filename)
    label = _model_test_one(svm_model_filename,feature_data)

    code = int(label[0])
    if int(code) >=0 and int(code) < len(string.printable):
        return (True,string.printable[int(code)])
    else:
        return (False,'')

def test():
    svm_model_filename = 'svm_model.txt'
    test_filename = 'test5.png'
    result = model_test_for_file(svm_model_filename,test_filename)
    print result


def main():
    svm_model_filename = 'svm_model.txt'
    #get train features:
    results = get_train_features('3CDEFHJKLMNWXY')
    #print len(results)

    import random
    random.shuffle(results)
    r_train = results[:int(len(results)*0.9)]
    r_test = results[int(len(results)*0.9):]
    #print len(r_train)
    #print len(r_test)
    with open('svm_train.txt','w') as f:
        for s in r_train:
            f.write(s)
            f.write(os.linesep)
    with open('svm_test.txt','w') as f:
        for s in r_test:
            f.write(s)
            f.write(os.linesep)

    _model_train('svm_train.txt',svm_model_filename)
    print ''
    _model_test('svm_model.txt','svm_test.txt')
    

if __name__ == '__main__':
    main()
    #test()
