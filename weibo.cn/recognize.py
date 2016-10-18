#!/usr/bin/env python
#-*- coding:utf-8 -*-
import split
import train

def main():
    svm_model_filename = 'svm_model.txt'
    #filename = 'test1.png'
    for i in range(1,6):
        filenames = split.split_one_file('test%s.png'%i)
        results = []
        for f in filenames:
            status,code = train.model_test_for_file(svm_model_filename,f)
            if status is True:
                results.append(code)

        print ''.join(results)


if __name__ == '__main__':
    main()